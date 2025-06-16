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

from spreadsheet_toolkit.csv_utils import get_csv_headers, read_csv_rows
from utilitycode.bom_utils import get_data_from_xlsx
from utilitycode.bom_utils import write_to_csv
from utilitycode.bom_utils import write_to_xlsx


def flattening(headers, result, key):
    """
    Flattening process and return the flattened data in a list of dictionary
    """
    sorted_result = sorted(result, key=lambda k: str(k[key]))
    flatten_list = []
    for i in sorted_result:
        if not flatten_list:
            flatten_list.append(i)
        else:
            if i[key] == flatten_list[-1][key]:
                for header_key in headers:
                    split_value = str(i[header_key]).splitlines()
                    for new_value in split_value:
                        original_value = str(flatten_list[-1][header_key])
                        if new_value and not new_value == original_value:
                            if '\n' in original_value:
                                if new_value in original_value.splitlines():
                                    continue
                                else:
                                    flatten_list[-1][header_key] = original_value + '\n' + \
                                        new_value if not original_value == '' else new_value
                            else:
                                flatten_list[-1][header_key] = original_value + '\n' + \
                                    new_value if not original_value == '' else new_value
            else:
                flatten_list.append(i)
    return flatten_list


@click.command()
@click.option('--csv',
              is_flag=True,
              help='Output as CSV format (Default: XLSX format)')
@click.option('-k', '--key',
              required=True,
              metavar='key',
              help='Key to be flatten.')
@click.argument('input', required=True, metavar='INPUT',
                type=click.Path(
                    exists=True, file_okay=True, dir_okay=True, readable=True,
                    resolve_path=True))
@click.argument('output', required=True, metavar='OUTPUT',
                type=click.Path(
                    exists=False, dir_okay=False, writable=True,
                    resolve_path=True))
@click.help_option('-h', '--help')
def cli(csv, key, input, output):
    """
    Flatten the input CSV/XLSX based on the provided key.
    """
    if not input.endswith('.csv') and not input.endswith('.xlsx'):
        raise click.UsageError(
            'ERROR: "The input does not ends with \'.csv\' or \'.xlsx\' extension.')

    if input.endswith('.csv'):
        headers = get_csv_headers(input)
        # Convert it with list to become a non-generator
        # object
        result = list(read_csv_rows(input))
    else:
        result, headers = get_data_from_xlsx(input)

    if key not in headers:
        print(key + " is not in the INPUT. Please correct and re-run.")
        return
    else:
        flatten_result = flattening(headers, result, key)
        if csv:
            if not output.endswith('.csv'):
                raise click.UsageError(
                    'ERROR: "The output does not ends with \'.csv\' extension.')
            else:
                write_to_csv(flatten_result, output)
        else:
            if not output.endswith('.xlsx'):
                raise click.UsageError(
                    'ERROR: "The output does not ends with \'.xlsx\' extension.')
            else:
                write_to_xlsx(flatten_result, output)
