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

"""
<?xml version="1.0" encoding="utf-8"?>
<licenses>
<file-name contentId="45d4ee055bdf34776905c04117951798">/vendor/bin/blah</file-name>


<file-content contentId="45d4ee055bdf34776905c04117951798"><![CDATA[

/*-
 * Copyright (c) blah blah
 *
 * This is under a public domain.
 */
]]></file-content>

</licenses>
"""

"""
The above is a sample of an AOSP notice xml file.
This utility will parse the `<file-name contentId="45d4ee055bdf34776905c04117951798">/vendor/bin/sh</file-name>`
to get the contentID and the reference path.
In addition, it will also capture the license texts within the
<file-content ... </file-content> and named as contentID
"""

is_license = False
file_name = ''
license_context = ''


def parse_aosp_notice(input):
    """
    Parse the contentID, reference path and capture the license text
    """
    id_reference = []
    id_license = []
    with open(input) as f:
        content = f.readlines()
        is_license = False
        license_context = ''
        for line in content:
            if line.strip():
                if '<file-name contentId=' in line:
                    dict = {}
                    name = line.partition('">')[0].partition('="')[2]
                    reference_path = line.partition(
                        '">')[2].partition('</file-name>')[0]
                    dict['contentID'] = name
                    dict['reference_path'] = reference_path
                    id_reference.append(dict)
                elif '<file-content contentId=' in line:
                    is_license = True
                    file_name = line.partition('="')[2].partition('">')[0]
                    license_context += line
                elif '></file-content>' in line:
                    license_context += line
                    is_license = False
                    dict = {}
                    dict[file_name] = license_context
                    id_license.append(dict)
                    is_license = False
                    file_name = ''
                    license_context = ''
                elif is_license:
                    license_context += line
    return id_reference, id_license


def write_license(id_license, lic_location):
    """
    Create captured licenses with the contentID as the filename and
    save it to the defined destination
    """
    for item in id_license:
        file_name = list(item.keys())[0]
        license_context = list(item.values())[0]
        output_lic_file = os.path.join(lic_location, file_name)
        lic_file = open(output_lic_file, "w")
        lic_file.write(license_context)
        lic_file.close()


@click.command()
@click.option('--csv',
              is_flag=True,
              help='Output as CSV format (Default: XLSX format)')
@click.argument('input', required=True, type=click.Path(exists=True, readable=True))
@click.argument('output', type=click.Path(exists=False), required=True)
@click.argument('lic_location', required=True,
                type=click.Path(
                    exists=True, file_okay=False, dir_okay=True, readable=True, resolve_path=True))
@click.help_option('-h', '--help')
def cli(csv, input, output, lic_location):
    """
    Take the AOSP XML Notice as an input. Parse the contentID,
    reference path and capture the license text. Save the contentID and the
    reference path to the output and save the captured licenses with the
    contentID as the filename to the lic_location.
    """
    id_reference, id_license = parse_aosp_notice(input)
    if csv:
        if not output.endswith('.csv'):
            raise click.UsageError(
                'ERROR: "The output does not ends with \'.csv\' extension.')
        else:
            write_to_csv(id_reference, output)
    else:
        if not output.endswith('.xlsx'):
            raise click.UsageError(
                'ERROR: "The output does not ends with \'.xlsx\' extension.')
        else:
            write_to_xlsx(id_reference, output)

    write_license(id_license, lic_location)
