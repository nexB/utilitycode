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
import codecs
import csv
import os
import sys

# silence unicode literals warnings
click.disable_unicode_literals_warning = True

on_windows = 'win32' in sys.platform

UNC_PREFIX = u'\\\\?\\'


def read_csv_rows(location):
    """
    Yield rows (as a list of values) from a CSV file at `location`.
    """
    with codecs.open(location, 'r', encoding='utf-8-sig', errors='replace') as csvfile:
        # add next line to deal with error "_csv.Error: field larger than field limit (131072)"
        # csv.field_size_limit(sys.maxsize)
        # The above is giving me "OverflowError: Python int too large to convert to C long" in Windows OS
        csv.field_size_limit(2147483647)
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row


def get_csv_headers(location):
    """
    Return a list of the column name of the input CSV.
    """
    headers = []
    with codecs.open(location, mode='r', encoding='utf-8-sig',
                     errors='replace') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        headers = csv_reader.fieldnames
    return headers


def add_unc(location):
    """
    Convert a `location` to an absolute Window UNC path to support long paths on
    Windows. Return the location unchanged if not on Windows. See
    https://msdn.microsoft.com/en-us/library/aa365247.aspx
    """
    if on_windows and not location.startswith(UNC_PREFIX):
        return UNC_PREFIX + os.path.abspath(location)
    return location


def write_csv(rows, output, col_names):
    with open(output, 'w', newline='', encoding='UTF-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=col_names)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
