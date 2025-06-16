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
import re

from spreadsheet_toolkit.csv_utils import get_csv_headers, read_csv_rows

from utilitycode.bom_utils import get_data_from_xlsx
from utilitycode.bom_utils import write_to_csv
from utilitycode.bom_utils import write_to_xlsx


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
                type=click.Path(exists=False, dir_okay=False, writable=True,
                                resolve_path=True))
@click.option('--csv',
              is_flag=True,
              help='Output as CSV format (Default: XLSX format)')
@click.option('--include', multiple=True,
              metavar='"key=string [or] key=string..."',
              help='Include the rows which the string exist in the key value.')
@click.option('--exclude', multiple=True,
              metavar='"key=string [or] key=string..."',
              help='Exclude the rows which the string exist in the key value.')
@click.option('--exclude_exact', multiple=True,
              metavar='"key=string [or] key=string..."',
              help='Exclude the rows which the string equals the key value.')
@click.option('--startswith', multiple=True,
              metavar='"key=string [or] key=string..."',
              help='Include the rows which the key value starts with the string.')
@click.option('--endswith', multiple=True,
              metavar='"key=string [or] key=string..."',
              help='Include the rows which the key value ends with the string.')
@click.option('--equals', multiple=True,
              metavar='"key=string [or] key=string..."',
              help='Include the rows which the string equals with the key value.')
@click.help_option('-h', '--help')
def cli(input, output, csv, include, exclude, exclude_exact, startswith, endswith, equals):
    """
    Filtering the input with the provided option(s).
    """
    if not input.endswith('.csv') and not input.endswith('.xlsx'):
        raise click.UsageError(
            'ERROR: "The input does not ends with \'.csv\' or \'.xlsx\' extension.')

    include_condition = []
    exclude_condition = []
    exclude_exact_condition = []
    startswith_condition = []
    endswith_condition = []
    equals_condition = []

    # Get the filter condition
    if include:
        include_condition = get_filtering_keys_values(include)
    if exclude:
        exclude_condition = get_filtering_keys_values(exclude)
    if exclude_exact:
        exclude_exact_condition = get_filtering_keys_values(exclude_exact)
    if startswith:
        startswith_condition = get_filtering_keys_values(startswith)
    if endswith:
        endswith_condition = get_filtering_keys_values(endswith)
    if equals:
        equals_condition = get_filtering_keys_values(equals)

    if input.endswith('.csv'):
        column_names = get_csv_headers(input)
        # Convert it with list to become a non-generator
        # object
        rows = list(read_csv_rows(input))
    else:
        rows, column_names = get_data_from_xlsx(input)

    # Validate the existance of the input keys
    filter_keys = []
    combined_condition = include_condition + exclude_condition + \
        exclude_exact_condition + startswith_condition + \
        endswith_condition + equals_condition
    for dict in combined_condition:
        keys = dict.keys()
        for key in keys:
            if key not in filter_keys:
                filter_keys.append(key)

    for key in filter_keys:
        if key not in column_names:
            import sys
            print("The key '" + key +
                  "' is not in the input. Please correct and re-run.")
            sys.exit(1)

    result = []
    for row in rows:
        if include:
            row = include_filtering(row, include_condition)
        if exclude:
            row = exclude_filtering(row, exclude_condition)
        if exclude_exact:
            row = exclude_exact_filtering(row, exclude_exact_condition)
        if startswith:
            row = startswith_filtering(row, startswith_condition)
        if endswith:
            row = endswith_filtering(row, endswith_condition)
        if equals:
            row = equals_filtering(row, equals_condition)
        if row:
            result.append(row)

    if csv:
        if not output.endswith('.csv'):
            raise click.UsageError(
                'ERROR: "The output does not ends with \'.csv\' extension.')
        else:
            write_to_csv(result, output)
    else:
        if not output.endswith('.xlsx'):
            raise click.UsageError(
                'ERROR: "The output does not ends with \'.xlsx\' extension.')
        else:
            write_to_xlsx(result, output)


def get_filtering_keys_values(expression):
    """
    Return lists of dictionary of filter condition.
    Each dictionary is under "and" condition while element in the
    dictionary is under "or" condition
    """
    exp_list = []
    expression = list(expression)
    for exp in expression:
        filter_dict = {}
        args = re.split(" or ", exp, flags=re.IGNORECASE)
        for arg in args:
            try:
                k, v = arg.split("=")
                if k not in filter_dict.keys():
                    filter_dict[k] = [v]
                else:
                    filter_dict[k].append(v)
            # Treat all non-empty value as filtered values
            except ValueError:
                k = arg
                filter_dict[k] = True
        exp_list.append(filter_dict)
    return exp_list


def include_filtering(input, include_condition):
    """
    Filter the input based on the include options provided from the user.
    """
    multi_condition = True if len(include_condition) > 1 else False
    condition_met = False
    for condition in include_condition:
        condition_met = False
        for key in condition.keys():
            # This will include everything that have value in the include key
            if isinstance(condition[key], bool):
                if input[key]:
                    return input
            else:
                for include_value in condition[key]:
                    if input:
                        if include_value in input[key]:
                            if not multi_condition:
                                return input
                            else:
                                condition_met = True
                                break
                if condition_met:
                    break
        if not condition_met:
            return
    if condition_met:
        return input


def exclude_filtering(input, exclude_condition):
    """
    Filter the input based on the exclude options provided from the user.
    """
    for condition in exclude_condition:
        for key in condition.keys():
            # This will exclude everything that have value in the exclude key
            # In another word, this will keep all the rows which its key's value
            # is empty
            if isinstance(condition[key], bool):
                if input[key]:
                    return
            else:
                for exclude_value in condition[key]:
                    if input:
                        if exclude_value in input[key]:
                            return
    return input


def exclude_exact_filtering(input, exclude_exact_condition):
    """
    Filter the input based on the exclude exact options provided from the user.
    """
    for condition in exclude_exact_condition:
        for key in condition.keys():
            # This will exclude everything that have value in the exclude key
            # In another word, this will keep all the rows which its key's value
            # is empty
            if isinstance(condition[key], bool):
                if input[key]:
                    return
            else:
                for exclude_value in condition[key]:
                    if input:
                        if exclude_value == input[key]:
                            return
    return input


def equals_filtering(input, equals_condition):
    """
    Filter the input based on the equals options provided from the user.
    """
    multi_condition = True if len(equals_condition) > 1 else False
    condition_met = False
    for condition in equals_condition:
        condition_met = False
        for key in condition.keys():
            for equals_value in condition[key]:
                if input:
                    if input[key] and input[key] == equals_value:
                        if not multi_condition:
                            return input
                        else:
                            condition_met = True
                            break
            if condition_met:
                break
        if not condition_met:
            return
    if condition_met:
        return input


def startswith_filtering(input, startswith_condition):
    """
    Filter the input based on the startswith options provided from the user.
    """
    multi_condition = True if len(startswith_condition) > 1 else False
    condition_met = False
    for condition in startswith_condition:
        condition_met = False
        for key in condition.keys():
            for startswith_value in condition[key]:
                if input:
                    if input[key] and input[key].startswith(startswith_value):
                        if not multi_condition:
                            return input
                        else:
                            condition_met = True
                            break
            if condition_met:
                break
        if not condition_met:
            return
    if condition_met:
        return input


def endswith_filtering(input, endswith_condition):
    """
    Filter the input based on the endswith options provided from the user.
    """
    multi_condition = True if len(endswith_condition) > 1 else False
    condition_met = False
    for condition in endswith_condition:
        condition_met = False
        for key in condition.keys():
            for endswith_value in condition[key]:
                if input:
                    if input[key] and input[key].endswith(endswith_value):
                        if not multi_condition:
                            return input
                        else:
                            condition_met = True
                            break
            if condition_met:
                break
        if not condition_met:
            return
    if condition_met:
        return input
