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
import string

from os.path import exists, dirname, join


def collect_and_write_bin_str(input, output, filter=False):
    # It is intentionally to write the output row by row immediately instead of
    # storing in a list to prevent memory error when working on huge data.
    if not output.endswith('.csv'):
        msg = u'The output has to be a CSV file.'
        raise Exception(msg)
    if not exists(dirname(output)):
        os.makedirs(dirname(output))

    header_row = ['Resource', 'binary_strings']

    with open(output, mode='w', encoding='utf-8', errors='ignore', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow(header_row)
        assert input

        if os.path.isdir(input):
            for root, dirs, files in os.walk(input):
                for file in files:
                    filepath = join(root, file)
                    relative_path = filepath.partition(input)[2]
                    bin_strings = list(strings(filepath))
                    for str in bin_strings:
                        if filter:
                            for f_string in filter:
                                if f_string.lower() in str.lower():
                                    csv_writer.writerow([relative_path, str])
                        else:
                            csv_writer.writerow([relative_path, str])
        else:
            bin_strings = list(strings(input))
            file_name = os.path.basename(input)
            for str in bin_strings:
                if filter:
                    for f_string in filter:
                        if f_string.lower() in str.lower():
                            csv_writer.writerow([file_name, str])
                else:
                    csv_writer.writerow([file_name, str])

# This is modified from https://stackoverflow.com/questions/17195924/python-equivalent-of-unix-strings-utility
def strings(filename, min=4):
    with open(filename, mode='r', encoding='utf-8', errors='ignore', newline='') as f:
        result = ""
        for c in f.read():
            if c in string.printable:
                result += c
                continue
            if len(result) >= min:
                result = result.strip()
                yield result
            result = ""
        if len(result) >= min:  # catch result at EOF
            result = result.strip()
            yield result


@click.command()
@click.argument('location', type=click.Path(exists=True, readable=True))
@click.argument('destination', type=click.Path(exists=False), required=True)
@click.option('--filter', multiple=True,
              type=str,
              help='Look for specific string in the binary_strings')
def cli(location, destination, filter):
    """
    Collect binary strings from file(s) and output to a CSV.
    """
    collect_and_write_bin_str(location, destination, filter)
