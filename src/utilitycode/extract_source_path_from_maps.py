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

from os.path import join
from utilitycode.bom_utils import write_to_csv
from utilitycode.bom_utils import write_to_xlsx


def extract_source_from_map(map_file):
    """
    Extract the source section for the input map file and return as a list.
    """
    result = []
    try:
        with open(map_file, encoding='utf-8', errors='ignore') as json_file:
            if json_file:
                data = json.load(json_file)
                for entry in data.get('sources'):
                    result.append(entry)
    except:
        print("Problematic file: " + map_file)
    return result


def format_data(path, data_list):
    """
    Return a list of dictionary in a desire format for output writing.
    """
    result = []
    for data in data_list:
        result.append({'Resource': path, 'extracted_source_path': data})
    return result


@click.command()
@click.option('--csv',
              is_flag=True,
              help='Output as CSV format (Default: XLSX format)')
@click.argument('input',
                required=True,
                metavar='INPUT',
                type=click.Path(
                    exists=True, file_okay=True, dir_okay=True, readable=True, resolve_path=True))
@click.argument('output',
                required=True,
                metavar='OUTPUT',
                type=click.Path(exists=False, dir_okay=False, writable=True, resolve_path=True))
@click.help_option('-h', '--help')
def cli(csv, input, output):
    """
    This utility is designed to extract source paths from .map files
    (.js.map / .css.map). These .map files contain multiple sections, but
    the primary focus of this utility is the "sources" section, which it will
    extract.
    """
    updated_data = []
    if os.path.isdir(input):
        for root, _dirs, files in os.walk(input):
            for file in files:
                if file.endswith('.map'):
                    filepath = join(root, file)
                    relative_path = filepath.partition(input)[2]
                    source_path_list = extract_source_from_map(filepath)
                    updated_data = updated_data + format_data(relative_path,
                                                              source_path_list)
    else:
        if input.endswith('.map'):
            source_path_list = extract_source_from_map(input)
            file_name = os.path.basename(input)
            updated_data = format_data(file_name, source_path_list)
        else:
            print("The input is not a map file.")

    if csv:
        if not output.endswith('.csv'):
            raise click.UsageError(
                'ERROR: "The output does not ends with \'.csv\' extension.')
        else:
            write_to_csv(updated_data, output)
    else:
        if not output.endswith('.xlsx'):
            raise click.UsageError(
                'ERROR: "The output does not ends with \'.xlsx\' extension.')
        else:
            write_to_xlsx(updated_data, output)
