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
import os

from utilitycode.bom_utils import write_to_csv
from utilitycode.bom_utils import write_to_xlsx


def get_package_list(input):
    """
    Return a list of file paths for all files with the '.md5sum' extension
    """
    path_list = []
    for root, _subdir, files in os.walk(input):
        for file in files:
            if file.endswith('.md5sums'):
                path_list.append(os.path.join(root, file))
    return path_list


def parse_process(path_list):
    """
    parse the md5sums data
    """
    parsed_data = []
    for path in path_list:
        f = open(path, "r")
        content = f.readlines()
        for line in content:
            filename = os.path.basename(path)
            md5_value, install_path = line.split(' ', 1)
            data_dict = {}
            data_dict['Resource'] = filename
            data_dict['md5'] = md5_value
            data_dict['installed_path'] = install_path.strip()
            parsed_data.append(data_dict)
    return parsed_data


@click.command()
@click.option('--csv',
              is_flag=True,
              help='Output as CSV format (Default: XLSX format)')
@click.argument('input', type=click.Path(exists=True, readable=True), required=True)
@click.argument('output', type=click.Path(exists=False), required=True)
@click.help_option('-h', '--help')
def cli(csv, input, output):
    '''
    Read the *.md5sums files under /var/lib/dpkg/info/ to get the file
    level installed path and the md5 value
    '''
    md5sums_list = get_package_list(input)
    data = parse_process(md5sums_list)

    if csv:
        write_to_csv(data, output)
    else:
        write_to_xlsx(data, output)
