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
import io
import os

from utilitycode import bom_utils


def parse_nuspec_file(input):
    """
    Parse the nuspec file and get the id, version, authors, owners,license,
    licenseUrl, projectUrl and copyright
    """
    content = {}
    with io.open(input, encoding="utf8", errors='ignore') as loc:
        result = loc.readlines()
        content['Resource'] = input
        for line in result:
            line = line.strip()
            if line.startswith('<id>'):
                content['id'] = strip_tags(line)
            elif line.startswith('<version'):
                content['version'] = strip_tags(line)
            elif line.startswith('<authors'):
                content['authors'] = strip_tags(line)
            elif line.startswith('<owners'):
                content['owners'] = strip_tags(line)
            elif line.startswith('<license type'):
                content['license'] = strip_tags(line)
            elif line.startswith('<licenseUrl'):
                content['licenseUrl'] = strip_tags(line)
            elif line.startswith('<projectUrl>'):
                content['projectUrl'] = strip_tags(line)
            elif line.startswith('<copyright>'):
                content['copyright'] = strip_tags(line)
    return content


def strip_tags(line):
    """
    strip the tag from the input
    """
    return line.partition('>')[2].rpartition('</')[0]


def formart_data_to_write(header, data):
    """
    Format the data to lists of list to be ready to write to XLSX
    """
    output_list = []
    output_list.append(header)
    for item in data:
        item_list = []
        for name in header:
            if name in item.keys():
                item_list.append(item[name])
            else:
                item_list.append('')
        output_list.append(item_list)
    return output_list


@click.command()
@click.argument('location', type=click.Path(exists=True, readable=True))
@click.argument('destination', type=click.Path(exists=False), required=True)
@click.help_option('-h', '--help')
def cli(location, destination):
    """
    This utility iterates through the specified directory, identifies files
    with the .nuspec extension, parses their content, and stores the
    extracted data in an XLSX output file.
    """
    info_list = []
    headers = ['Resource', 'id', 'version', 'authors', 'owners', 'license',
               'licenseUrl', 'projectUrl', 'copyright']
    if os.path.isfile(location) and location.endswith('.nuspec'):
        info_dict = parse_nuspec_file(location)
        info_list.append(info_dict)
    else:
        for root, _subdirs, files in os.walk(location):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.endswith('.nuspec'):
                    info_dict = parse_nuspec_file(file_path)
                    info_list.append(info_dict)

    output = formart_data_to_write(headers, info_list)

    bom_utils.create_xlsx_output(destination, output)
    click.echo('Saving BOM to %s' % destination)
