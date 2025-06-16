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

from os.path import join

from utilitycode.utils import to_posix
from utilitycode.bom_utils import write_to_csv
from utilitycode.bom_utils import write_to_xlsx


def get_package_file(input_location):
    """
    Return a list contains absolute path for all the files-in-package.txt
    """
    assert input_location
    file_list = []
    if os.path.isdir(input_location):
        for root, dirs, files in os.walk(input_location):
            for file in files:
                if file == 'files-in-package.txt':
                    filepath = join(root, file)
                    file_list.append(filepath)
    else:
        file_list.append(input_location)
    return file_list


def get_package_path_data(file_list, input_location):
    """
    Return a list of dictionaries with data found in "files-in-package.txt"
    """
    data = []
    for filepath in file_list:
        with open(filepath, "r") as f:
            text = f.read()
            lines = text.splitlines(False)
            result = {}

            # Convert path to posixpath
            input_posix = to_posix(input_location)
            posix_filepath = to_posix(filepath)

            if input_posix == posix_filepath:
                relative_resource_path = posix_filepath
            else:
                relative_resource_path = posix_filepath.partition(input_posix)[
                    2]
            f_list = []

            for line in lines:
                row = line.split()
                # row[0] is the file type and permission and we are looking
                # for '-' which is a file (not directory or link) type
                # row[4] is the install path information
                if not row[0].startswith('-'):
                    continue
                else:
                    f_list.append(row[4])
            if f_list:
                package_name = os.path.dirname(
                    relative_resource_path).rpartition('/')[2]
                result['Resource'] = relative_resource_path
                result['Package'] = package_name
                result['installed_path'] = f_list
                data.append(result)
    return data


def pre_process_data(data):
    """
    Unflatten the 'installed_path' so that each dictionary contains a
    single 'installed_path' entry. If multiple values exist in
    'installed_path', separate entries will be created accordingly.
    i.e.
    [
        {'Resource': 'logger/logger/files-in-package.txt', 'Package':'logger',
        'installed_path': ['./lib/liblogger_ldplugin.so', './usr/sbin/logger']}
    ]

    to

    [
        {'Resource': 'logger/logger/files-in-package.txt', 'Package': 'logger',
        'installed_path': './lib/liblogger_ldplugin.so'},
        {'Resource': 'logger/logger/files-in-package.txt', 'Package':
        'logger', 'installed_path': './usr/sbin/logger'}
    ]
    """
    formatted_data = []
    for entry in data:
        for path_value in entry['installed_path']:
            entry_dict = {}
            entry_dict['Resource'] = entry['Resource']
            entry_dict['Package'] = entry['Package']
            entry_dict['installed_path'] = path_value
            formatted_data.append(entry_dict)
    return formatted_data


@click.command()
@click.option('--csv',
              is_flag=True,
              help='Output as CSV format (Default: XLSX format)')
@click.argument('location', type=click.Path(exists=True, readable=True))
@click.argument('output', type=click.Path(exists=False), required=True)
@click.help_option('-h', '--help')
def cli(location, output, csv):
    """
    Parse and collect package's installed path from files-in-package.txt.
    The input can be a directory or a file.
    """
    file_list = get_package_file(location)
    data = get_package_path_data(file_list, location)
    process_data = pre_process_data(data)
    if csv:
        if not output.endswith('.csv'):
            raise click.UsageError(
                'ERROR: "The output does not ends with \'.csv\' extension.')
        else:
            write_to_csv(process_data, output)
    else:
        if not output.endswith('.xlsx'):
            raise click.UsageError(
                'ERROR: "The output does not ends with \'.xlsx\' extension.')
        else:
            write_to_xlsx(process_data, output)
