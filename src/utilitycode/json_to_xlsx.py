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
import openpyxl
import sys


@click.command()
@click.argument('input',
                required=True,
                metavar='INPUT',
                type=click.Path(
                    exists=True, file_okay=True, dir_okay=True, readable=True,
                    resolve_path=True))
@click.argument('output',
                required=True,
                metavar='OUTPUT',
                type=click.Path(
                    file_okay=True, dir_okay=False, writable=True,
                    resolve_path=True))
@click.help_option('-h', '--help')
def cli(input, output):
    """
    Convert a JSON file (list of directories) to a XLSX output
    """
    if not input.endswith('.json'):
        print("The input has to be a .json file.")
        sys.exit(1)
    if not output.endswith('.xlsx'):
        print("The output has to be a .xlsx file.")
        sys.exit(1)

    # Create a new workbook and select the active worksheet
    wb = openpyxl.Workbook()
    ws = wb.active

    with open(input, 'r', encoding='utf-8') as f:
        data = json.load(f)

    headers, rows = json_to_xlsx(data)

    # Write headers to the worksheet
    ws.append(headers)

    for row in rows:
        ws.append(row)

    wb.save(output)
    print("Finished. Saved to {output}")


def json_to_xlsx(data):
    """
    Load the JSON data and return the headers along with a list of rows,
    where each row is represented as a list of values.
    """
    # Check if the data is a list of dictionaries
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        # Get headers
        headers = []
        for item in data:
            for key in item.keys():
                if key not in headers:
                    headers.append(key)

        # Get rows
        rows = []
        for item in data:
            row = [item.get(key, '') for key in headers]
            rows.append(row)
    else:
        raise ValueError("JSON format must be a list of dictionaries.")

    return headers, rows
