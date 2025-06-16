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

import os
import sys

import click
import openpyxl


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
                type=click.Path(
                    file_okay=True, dir_okay=False, writable=True,
                    resolve_path=True))
@click.help_option('-h', '--help')
def cli(input, output):
    """
    Extract the LKM statements.
    i.e. linux/module.h, MODULE_LICENSE
    """
    if not output.endswith('.xlsx'):
        print("The output has to be a .XLSX file.")
        sys.exit(1)
    # Create a new workbook and select the active worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "LKM"

    # Write headers to the worksheet
    ws.append(["path", "lkm"])

    if os.path.isdir(input):
        for filename in os.listdir(input):
            file_path = os.path.join(input, filename)
            if os.path.isfile(file_path):
                lkm_statment_list = extract_lkm_stataments(file_path)
                for statement in lkm_statment_list:
                    ws.append([filename, statement])
    else:
        lkm_statment_list = extract_lkm_stataments(input)
        for statement in lkm_statment_list:
            ws.append([filename, statement])
    wb.save(output)


def extract_lkm_stataments(file_path):
    """
    Read the file line by line, extract the
    lkm statments and return as a list
    """
    lkm_statment_list = []
    with open(file_path, "r") as file:
        for line in file:
            if "linux/module.h" in line or "MODULE_LICENSE" in line:
                lkm_statment_list.append(line.strip())
    return lkm_statment_list
