#!/usr/bin/env python
# -*- coding: utf8 -*-

# ============================================================================
#  Copyright (c) nexB Inc. http://www.nexb.com/ - All rights reserved.
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  SPDX-License-Identifier: Apache-2.0
# ============================================================================

import click
import json
import os
import requests
import sys

from utilitycode.utils import shorten_filename

@click.command()
@click.argument(
    "input",
    required=True,
    metavar="INPUT",
    type=click.Path(
        exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True
    ),
)
@click.argument(
    "output",
    required=True,
    metavar="OUTPUT",
    type=click.Path(file_okay=False, dir_okay=True, writable=True, resolve_path=True),
)
@click.help_option("-h", "--help")
def cli(input, output):
    """
    Take an SCTK JSON input that has '"--license-text": true' and pull out
    each detected license’s matched_text. Save each one into its own file,
    using the identifier as the filename, in a directory.
    """
    if not input.endswith(".json"):
        print("The input has to be a SCTK produced .json file.")
        sys.exit(1)

    with open(input, "r", encoding="utf-8") as f:
        data = json.load(f)

    tool_name = data["headers"][0]["tool_name"]
    if tool_name != "scancode-toolkit":
        print("The input has to be a SCTK produced .json file.")
        sys.exit(1)

    license_detections_data_list = data["license_detections"]

    extracted_data_dict = extract_matched_text(license_detections_data_list)
    save_to_files(extracted_data_dict, output)

    print(
        f"Extracted {len(extracted_data_dict)} matched_texts from {input} and saved them to {output}."
    )


def extract_matched_text(license_detections_data_list):
    """
    Extract the matched_text for each detected license from the
    license_detections data list. Use the rule_identifier as the key and
    the matched_text as the value in a dictionary.
    """
    extracted_data = {}
    handled_rule_urls = set()
    should_fetch = []
    for license_detection in license_detections_data_list:
        identifier = license_detection["identifier"]
        reference_matches = license_detection["reference_matches"]
        matched_text_list = []
        for reference_match in reference_matches:
            if not reference_match['rule_url'] in handled_rule_urls:
                handled_rule_urls.add(reference_match['rule_url'])
                if is_rule_url_notice_text(reference_match['rule_url']):
                    should_fetch.append(reference_match['rule_url'])
                    if not reference_match["matched_text"] in matched_text_list:
                        updated_matched_text = reference_match["license_expression_spdx"] + ":\n\n" + reference_match["matched_text"]
                        matched_text_list.append(updated_matched_text)
            else:
                if reference_match['rule_url'] in should_fetch:
                    if not reference_match["matched_text"] in matched_text_list:
                        updated_matched_text = reference_match["license_expression_spdx"] + ":\n\n" + reference_match["matched_text"]
                        matched_text_list.append(updated_matched_text)

        if matched_text_list:
            matched_text = '\n\n\n'.join(f"{text}" for text in matched_text_list)
            filename = shorten_filename(identifier)
            extracted_data[filename] = matched_text
    return extracted_data

def save_to_files(data_dict, output_dir):
    """
    Save the extracted matched_text data to individual text files in the
    output directory.
    """
    for matched_rule in data_dict:
        filename = f"{matched_rule}"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(str(data_dict[matched_rule]))



def github_to_raw(url: str) -> str:
    """
    Convert GitHub file URLs (tree/blob) into raw.githubusercontent.com links.
    """
    if "github.com" in url:
        parts = url.split("/")
        user, repo = parts[3], parts[4]
        branch = parts[6]
        path = "/".join(parts[7:])
        raw_url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}"
        return raw_url
    else:
        raise ValueError("Not a valid GitHub URL")


def has_license_notice_or_text(content: str) -> bool:
    """
    Return True if the content contains either
    'is_license_notice: yes' or 'is_license_text: yes'.
    """
    for key in ["is_license_notice: yes", "is_license_text: yes"]:
        if key in content:
            return True
    return False

def is_rule_url_notice_text(url):
    try:
        if url.endswith('.LICENSE'):
            return True
        raw_url = github_to_raw(url)
        response = requests.get(raw_url)
        response.raise_for_status()
        if has_license_notice_or_text(response.text):
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
