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

from spreadsheet_toolkit.csv_utils import read_csv_rows

from utilitycode.bom_utils import get_data_from_xlsx
from utilitycode.bom_utils import write_to_csv
from utilitycode.bom_utils import write_to_xlsx


def keep_column(result, keep_cols):
    """
    Keep only the defined column's data
    """
    rows = []
    for i in result:
        row_dict = {}
        for k in keep_cols:
            row_dict[k] = i[k]
        rows.append(row_dict)
    return rows


@click.command()
@click.option('--csv',
              is_flag=True,
              help='Output as CSV format (Default: XLSX format)')
@click.option('-k', '--key',
              metavar='key',
              help='Column(s) to be kept.')
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
                    exists=False, dir_okay=False, writable=True,
                    resolve_path=True))
@click.help_option('-h', '--help')
def cli(csv, key, input, output):
    """
    Take the input CSV/XLSX and keep the defined columns and write to the
    output CSV/XLSX
    """
    if not input.endswith('.csv') and not input.endswith('.xlsx'):
        raise click.UsageError(
            'ERROR: "The input does not ends with \'.csv\' or \'.xlsx\' extension.')
    result = []
    headers = []

    if input.endswith('.csv'):
        result = read_csv_rows(input)
        for row in result:
            headers = list(row.keys())
            break
    else:
        result, headers = get_data_from_xlsx(input)

    keep_cols = key.split(',')
    for k in keep_cols:
        if k not in headers:
            print(k + " is not in the INPUT. Please correct and re-run.")
            return

    new_result = keep_column(result, keep_cols)

    if csv:
        if not output.endswith('.csv'):
            raise click.UsageError(
                'ERROR: "The output does not ends with \'.csv\' extension.')
        else:
            write_to_csv(new_result, output)
    else:
        if not output.endswith('.xlsx'):
            raise click.UsageError(
                'ERROR: "The output does not ends with \'.xlsx\' extension.')
        else:
            write_to_xlsx(new_result, output)
