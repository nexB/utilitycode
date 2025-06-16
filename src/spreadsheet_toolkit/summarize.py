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
import os
import sys

from spreadsheet_toolkit.csv_utils import get_csv_headers, read_csv_rows
from spreadsheet_toolkit import flatten

from utilitycode.bom_utils import get_data_from_xlsx
from utilitycode.bom_utils import write_to_csv
from utilitycode.bom_utils import write_to_xlsx


@click.command()
@click.argument('input',
                required=True,
                metavar='INPUT',
                type=click.Path(
                    exists=True, file_okay=True, dir_okay=False, readable=True,
                    resolve_path=True))
@click.argument('output',
                required=True,
                metavar='OUTPUT',
                type=click.Path(
                    file_okay=True, dir_okay=False, writable=True,
                    resolve_path=True))
@click.option('--csv',
              is_flag=True,
              help='Output as CSV format (Default: XLSX format)')
@click.option('-k', '--key',
              required=True,
              metavar='key',
              help='Key to be summarized.')
@click.help_option('-h', '--help')
def cli(input, output, csv, key):
    """
    Summarize the key data in the input from file level to directory level.
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

    if 'Resource' not in headers:
        print("Resource column is required. Please correct and re-run.")
        sys.exit(1)
    if key not in headers:
        print(key + " is not in the INPUT. Please correct and re-run.")
        sys.exit(1)

    summarized_list = summarize(result, key)
    output_headers = ['Resource', key]
    updated_result = flatten.flattening(
        output_headers, summarized_list, 'Resource')

    if csv:
        if not output.endswith('.csv'):
            raise click.UsageError(
                'ERROR: "The output does not ends with \'.csv\' extension.')
        else:
            write_to_csv(updated_result, output)
    else:
        if not output.endswith('.xlsx'):
            raise click.UsageError(
                'ERROR: "The output does not ends with \'.xlsx\' extension.')
        else:
            write_to_xlsx(updated_result, output)


def summarize(result, key):
    """
    Summarize the key data in the input CSV from file level to directory level.
    """
    summarized_list = []
    for row in result:
        if row[key]:
            path = row['Resource']
            all_parents = get_all_parents(path)
            for dir in all_parents:
                dict = {}
                dict['Resource'] = dir + '/'
                dict[key] = row[key]
                summarized_list.append(dict)
    return summarized_list


def get_all_parents(path):
    """
    Return all the parent dirs (recursively) in a list
    """
    dir_list = []
    p = path
    while '/' in p and not p == '/':
        p = os.path.dirname(p)
        if not p == '/':
            dir_list.append(p)
    return dir_list
