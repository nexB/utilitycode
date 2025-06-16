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

import click
from debian_inspector import debcon

from utilitycode.bom_utils import write_to_csv
from utilitycode.bom_utils import write_to_xlsx
from utilitycode.bom_utils import write_to_json


def parse_status(input):
    """
    Use the debian-inspector library to parse the status file
    """
    result = debcon.get_paragraphs_data_from_file(input)
    return list(result)


@click.command()
@click.argument('input', type=click.Path(exists=True, readable=True), required=True)
@click.argument('output', type=click.Path(exists=False), required=True)
@click.option('--csv',
              is_flag=True,
              help='Output as CSV format (Default: XLSX format)')
@click.option('--json',
              is_flag=True,
              help='Output as JSON format (Default: XLSX format)')
@click.help_option('-h', '--help')
def cli(input, output, csv, json):
    '''
    Read the /var/lib/dpkg/status file (status for the installed packages) and
    do the parsing using the debian-inspector library.
    '''
    parsed_data = parse_status(input)
    if json:
        if not output.endswith('.json'):
            raise click.UsageError(
                'ERROR: "The output does not ends with \'.json\' extension.')
        else:
            write_to_json(parsed_data, output)
    elif csv:
        if not output.endswith('.csv'):
            raise click.UsageError(
                'ERROR: "The output does not ends with \'.csv\' extension.')
        else:
            write_to_csv(parsed_data, output)
    else:
        if not output.endswith('.xlsx'):
            raise click.UsageError(
                'ERROR: "The output does not ends with \'.xlsx\' extension.')
        else:
            write_to_xlsx(parsed_data, output)
