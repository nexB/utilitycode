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

from __future__ import absolute_import, print_function

from license_expression import Licensing
from utilitycode.bom_utils import create_xlsx_output
from utilitycode.bom_utils import format_dict_data_for_xlsx_output
from utilitycode.bom_utils import get_data_from_xlsx

import click
import copy


def write_output(data, output):
    """
    Write to output
    """
    formatted_data = format_dict_data_for_xlsx_output(data)
    create_xlsx_output(output, formatted_data)


def dedup_license_expression(rows_list):
    """
    Get the expression value from the 'license_expression' and
    pass it to the `license-expression` library for deduplication, and
    then update the result
    """
    deduped_lic_exp_result = []
    licensing = Licensing()
    for row in rows_list:
        row_dict = copy.deepcopy(row)
        expression = row['license_expression']
        if expression:
            try:
                deduped_exp = licensing.dedup(expression)
                row_dict['normailize_license_expression'] = str(deduped_exp)
            except:
                # Keep normalizing even if there is error
                pass
        else:
            row_dict['normailize_license_expression'] = row['license_expression']
        deduped_lic_exp_result.append(row_dict)
    return deduped_lic_exp_result


@click.command()
@click.argument('input', type=click.Path(exists=True, readable=True), required=True)
@click.argument('output', type=click.Path(exists=False), required=True)
@click.help_option('-h', '--help')
def cli(input, output):
    '''
    Read the license_expression field from the input XLSX and perfrom
    deduplication and then write to the output
    '''
    result, header = get_data_from_xlsx(input)
    if not input.endswith('.xlsx') and not output.endswith('.xlsx'):
        raise click.UsageError(
            'ERROR: Invalid input/output file extension: must be .xlsx.')
    if 'license_expression' not in header:
        raise click.UsageError(
            'The input does not have the `license_expression` field.')
    updated_result = dedup_license_expression(result)
    write_output(updated_result, output)
