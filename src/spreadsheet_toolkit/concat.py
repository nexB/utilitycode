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

# silence unicode literals warnings
click.disable_unicode_literals_warning = True


def concat_inputs(input, ws):
    """
    Get all rows from the input(s) in OrderedDict format, store them, and
    return as a list.
    """
    concat_rows = []
    for i in input:
        if i.endswith('.csv'):
            rows = read_csv_rows(i)
        else:
            rows, _headers = get_data_from_xlsx(i, ws)
        for row in rows:
            concat_rows.append(row)
    return concat_rows


def sync_rows_dict(rows):
    """
    Sync the dictionary keys by inserting any missing keys with an empty
    value if they are not present in the original dictionary.
    """
    dict_keys = []
    new_list = []
    # Collect all the keys from the list
    for row in rows:
        for key in row:
            if key not in dict_keys:
                dict_keys.append(key)

    for row in rows:
        for k in dict_keys:
            if k not in row:
                row[k] = ""
        new_list.append(row)
    return new_list


@click.command()
@click.option('--csv',
              is_flag=True,
              help='Output as CSV format (Default: XLSX format)')
@click.option(
    '-ws', '--worksheet', nargs=1,
    help='Define the name of the worksheet to work on for the XLSX input.'
)
@click.option('-i', '--input', multiple=True,
              metavar='FILE',
              type=click.Path(exists=True, dir_okay=False,
                              readable=True, resolve_path=True),
              help='Path to the input file.')
@click.option('-o', '--output',
              metavar='OUTPUT',
              type=click.Path(exists=False, dir_okay=False,
                              writable=True, resolve_path=True),
              help='Path to the concatenated output file.')
@click.help_option('-h', '--help')
def cli(csv, worksheet, input, output):
    """
    Concatenate the input CSV/XLSX files and write to a new CSV/XLSX (-o) file.
    Multiple '-i' options are supported.
    """
    rows = concat_inputs(input, worksheet)
    new_result = sync_rows_dict(rows)
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
