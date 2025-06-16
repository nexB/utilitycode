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
import csv
import os
import io

from debian_inspector import copyright

from utilitycode.bom_utils import write_to_csv
from utilitycode.bom_utils import write_to_xlsx


def get_copyright_files(input):
    list_of_files = []
    for (dirpath, _dirnames, filenames) in os.walk(input):
        for filename in filenames:
            if filename == 'copyright':
                list_of_files.append(os.sep.join([dirpath, filename]))
    return list_of_files


def parse_copyright(input):
    data = copyright.DebianCopyright.from_file(input).to_dict()
    useful_data = data['paragraphs']
    data_list = []
    header = []
    for item_dict in useful_data:
        if 'files' in item_dict:
            data_list.append(item_dict)
            head_keys = item_dict.keys()
            for k in head_keys:
                if not k in header:
                    header.append(k)
    return data_list, header


def write_csv(rows, output, col_names):
    with open(output, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=col_names)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def format_output(data_dict):
    output_list = []
    data_list = list(data_dict.values())
    path = data_dict.keys()
    index = 0
    for p in path:
        path_data_list = data_list[index]
        for data in path_data_list:
            updated_dict = {}
            updated_dict['path'] = p
            for k in data.keys():
                # updated_dict[k] = data[k].encode("utf-8")
                updated_dict[k] = data[k]
            output_list.append(updated_dict)
        index = index + 1
    return output_list


@click.command()
@click.option('--csv',
              is_flag=True,
              help='Output as CSV format (Default: XLSX format)')
@click.argument('input', type=click.Path(exists=True, readable=True), required=True)
@click.argument('output', type=click.Path(exists=False), required=True)
@click.help_option('-h', '--help')
def cli(csv, input, output):
    '''
    Parse the debian's copyright file to get the information for "Files",
    "License", "Copyright", "Comment"
    '''
    data_dictionary = {}
    errors = []
    headers = ['path']
    if os.path.isfile(input) and os.path.basename(input) == 'copyright':
        result, headers = parse_copyright(input)
        data_dictionary[input] = result
    else:
        copyright_files = get_copyright_files(input)
        for f in copyright_files:
            try:
                result, header = parse_copyright(f)
                data_dictionary[f] = result
                for h in header:
                    if not h in headers:
                        headers.append(h)
            except Exception as e:
                msg = 'Parsing error for ' + f + ": " + str(e)
                errors.append(msg)
                continue

    if data_dictionary:
        output_data = format_output(data_dictionary)
        if csv:
            write_to_csv(output_data, output)
        else:
            write_to_xlsx(output_data, output)

    if errors:
        output_parent = os.path.dirname(output)
        err_output = os.path.join(output_parent, 'error.txt')
        with io.open(err_output, mode='w', encoding='utf-8') as f:
            for e in errors:
                f.write(e + os.linesep)
