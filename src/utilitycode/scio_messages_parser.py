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

from utilitycode.bom_utils import create_xlsx_output
from utilitycode.bom_utils import format_dict_data_for_xlsx_output
from utilitycode.bom_utils import get_data_from_xlsx


def remove_first_space(string):
    # Split the string into lines
    lines = string.split("\n")
    # Remove leading space from each line
    modified_lines = [line.lstrip(" ") for line in lines]
    # Join the modified lines back together
    modified_string = "\n".join(modified_lines)
    return modified_string


def extract_messages_data(results_list):
    """
    Keep the "uuid" and extract the "name", "version", "datafile_path",
    "declared_license_expression" and "extracted_license_statement" from the
    "details" field
    """
    output_list = []
    for message in results_list:
        message_dict = {}
        message_dict['uuid'] = message['uuid']
        details = message['details']
        name = details.partition('name: ')[2].partition('\n')[0].strip()
        version = details.partition('version: ')[2].partition('\n')[0].strip()
        datafile_paths = details.partition('datafile_paths: ')[
            2].partition('\n')[0].strip()
        declared_license_expression = details.partition('declared_license_expression: ')[
            2].partition('\n')[0].strip()
        statement = details.partition('extracted_license_statement')[2]
        if "|" in statement:
            extracted_license_statement = remove_first_space(
                statement.partition('|')[2].strip())
        else:
            extracted_license_statement = statement.partition(':')[2].strip()
        message_dict['name'] = name
        message_dict['version'] = version
        message_dict['datafile_paths'] = datafile_paths
        message_dict['declared_license_expression'] = declared_license_expression
        message_dict['extracted_license_statement'] = extracted_license_statement

        # Create a deep copy of the dictionary
        copied_dict = copy.deepcopy(message_dict)
        output_list.append(copied_dict)
    return output_list


@click.command()
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument("output", type=click.Path(exists=False), required=True)
@click.help_option('-h', '--help')
def cli(input, output):
    """
    This utility extracts data from the "details" column in the "MESSAGES"
    worksheet from SCIO's XLSX output.
    The parsed data will be saved to the xlsx output.
    Following are the sample that list the fields that need to be parsed:

        \b
        name:
        version:
        datafile_paths: []
        declared_license_expression: gpl-2.0-plus OR lgpl-2.1-plus
        extracted_license_statement: |
            GPL-2.0+
            LGPL-2.1+
    """
    worksheet_name = "MESSAGES"

    results, _headers = get_data_from_xlsx(input, worksheet_name)
    output_list = extract_messages_data(results)
    data = format_dict_data_for_xlsx_output(output_list)
    create_xlsx_output(output, data)
