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
import os
import sys

from spreadsheet_toolkit.csv_utils import add_unc
from spreadsheet_toolkit.csv_utils import get_csv_headers
from spreadsheet_toolkit.csv_utils import read_csv_rows
from utilitycode.bom_utils import get_data_from_xlsx

# silence unicode literals warnings
click.disable_unicode_literals_warning = True
on_windows = 'win32' in sys.platform


def get_resource_path(rows, parent):
    """
    Get the path and validate the existences
    """
    errors = []
    copy_resource = []
    for row in rows:
        path = row['Resource']
        resource_path = os.path.normpath(os.path.join(parent, path))
        if on_windows:
            resource_path = add_unc(resource_path)

        if not os.path.exists(resource_path):
            errors.append(resource_path)
        else:
            copy_resource.append(resource_path)
    return errors, copy_resource


def copy_resources(output, copy_path, zip):
    """
    Copy/Zip the resource path to the destination
    """
    if zip:
        import zipfile
        with zipfile.ZipFile(output, 'w') as output_zip:
            for resource_path in copy_path:
                output_zip.write(resource_path)
    else:
        import shutil
        for resource_path in copy_path:
            try:
                shutil.copy2(resource_path, output)
            except Exception as e:
                print(repr(e))
                print('Cannot copy file at %(resource_path)r.' % locals())


@click.command()
@click.argument('input',
                required=True,
                metavar='INPUT',
                type=click.Path(
                    exists=True, file_okay=True,
                    dir_okay=True, readable=True, resolve_path=True))
@click.argument('project_loc',
                required=True,
                metavar='Project_Location',
                type=click.Path(
                    exists=True, file_okay=False,
                    dir_okay=True, readable=True, resolve_path=True))
@click.argument('output',
                required=True,
                metavar='OUTPUT',
                type=click.Path(file_okay=True,
                                dir_okay=True, writable=True,
                                resolve_path=True))
@click.option('--zip',
              is_flag=True,
              help='Output the copied content to a zip file.')
@click.help_option('-h', '--help')
def cli(input, project_loc, output, zip):
    """
    Copy/Zip the resource paths listed in the input from the project_loc to
    the output location.
    """
    if not input.endswith('.csv') and not input.endswith('.xlsx'):
        raise click.UsageError(
            'ERROR: "The input does not ends with \'.csv\' or \'.xlsx\' extension.')

    if input.endswith('.csv'):
        headers = get_csv_headers(input)
        # Convert it with list to become a non-generator
        # object
        result = list(read_csv_rows(input))
    else:
        result, headers = get_data_from_xlsx(input)

    # Validate does the input has the 'Resource' header
    if 'Resource' not in headers:
        print("`Resource` is not in the INPUT. Please correct and re-run.")
        return

    if zip and os.path.exists(output):
        print("The output zip file already exist. Please remove and re-run.")
        return

    if not os.path.exists(output) and not zip:
        os.mkdir(output)

    parent = os.path.dirname(project_loc)

    errors, copy_path = get_resource_path(result, parent)
    copy_resources(output, copy_path, zip)

    if errors:
        print("The following path does not exist:")
        for e in errors:
            print(e)
