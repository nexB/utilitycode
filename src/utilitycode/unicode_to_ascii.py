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
import copy

from commoncode import text

from spreadsheet_toolkit.csv_utils import read_csv_rows

from utilitycode.bom_utils import get_data_from_xlsx
from utilitycode.bom_utils import write_to_csv
from utilitycode.bom_utils import write_to_xlsx


@click.command()
@click.argument('input',
                required=True,
                metavar='INPUT',
                type=click.Path(
                    exists=True, file_okay=True, dir_okay=True, readable=True, resolve_path=True))
@click.argument('output',
                required=True,
                metavar='OUTPUT',
                type=click.Path(exists=False, dir_okay=False, writable=True, resolve_path=True))
@click.option('--worksheet',
              metavar='name',
              help='The worksheet name from the INPUT. (Default: the "active" worksheet)')
@click.help_option('-h', '--help')
def cli(input, output, worksheet):
    """
    Detect if the input (CSV/XLSX) contains any unicode Mark an "x" in a
    "Unicode Detected" column and proposed correction in the output.
    """
    if not input.endswith('.csv') and not input.endswith('.xlsx'):
        raise click.UsageError(
            'ERROR: "The input does not ends with \'.csv\' or \'.xlsx\' extension.')
    if not output.endswith('.csv') and not output.endswith('.xlsx'):
        raise click.UsageError(
            'ERROR: "The output does not ends with \'.csv\' or \'.xlsx\' extension.')
    if worksheet and not input.endswith('.xlsx'):
        raise click.UsageError(
            'ERROR: --worksheet option only works with .xlsx input.')

    if input.endswith('.csv'):
        # Convert it with list to become a non-generator
        # object
        rows = list(read_csv_rows(input))
    else:
        rows, _column_names = get_data_from_xlsx(input, worksheet)

    result, unicode_detected = check_unicode(rows)

    if not unicode_detected:
        print("No unicode detected. Nothing is generated.")
    else:
        if output.endswith('.csv'):
            write_to_csv(result, output)
        else:
            write_to_xlsx(result, output)


def check_unicode(rows):
    """
    Check if the list of dictionary contains any unicode value
    Output the origianl input with new unicode detected and correction
    columns at the far right
    """
    result = []
    unicode_detected = False
    for row in rows:
        new_dict = dict()
        issue_dict = dict()
        for key in row:
            value = str(row[key])
            new_dict[key] = value
            try:
                value.encode('ascii')
            except UnicodeEncodeError:
                unicode_detected = True
                issue_dict['Unicode Detected'] = 'x'
                corrected_key_name = 'Ignored Unicode - ' + key
                issue_dict[corrected_key_name] = text.toascii(value)

        update_dict = copy.deepcopy(issue_dict)
        issue_dict.clear()
        for d in update_dict:
            new_dict[d] = update_dict[d]
        result.append(new_dict)
    return result, unicode_detected
