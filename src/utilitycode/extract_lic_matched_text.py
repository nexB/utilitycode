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
import sys


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
    using the rule_identifier as the filename, in a directory.
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
    for license_detection in license_detections_data_list:
        reference_matches = license_detection["reference_matches"]
        for reference_match in reference_matches:
            rule_identifier = reference_match["rule_identifier"]
            matched_text = reference_match["matched_text"]
            extracted_data[rule_identifier] = matched_text
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
