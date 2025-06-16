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

import requests

import click
import openpyxl

from utilitycode import bom_utils

# TODO: add this function to bom_utils


def output_results(destination, results):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(('Gem Name', 'Version', 'Owner', 'License', 'Download URL'))
    for result in results:
        ws.append(result)

    click.echo('Saving Gem Analysis to %s' % destination)
    wb.save(destination)


def get_gem_metadata(gems):
    print('Working...')

    results = []
    for name, version in gems:
        response = requests.get(
            'https://rubygems.org/api/v1/versions/{}.json'.format(name))
        if response.status_code == requests.codes.ok:
            gem_versions = response.json()
            for gem in gem_versions:
                gem_version = gem.get('number')
                if version == gem_version:
                    licenses, author = gem.get('licenses'), gem.get('authors')

                    # TODO: handle this better
                    if isinstance(licenses, list):
                        license = ', '.join(licenses)
                    else:
                        license = licenses

                    download_url = 'https://rubygems.org/gems/{}-{}.gem'.format(
                        name, version)
                    results.append((name, 'v {}'.format(version),
                                   author, license, download_url))
                    break
    return results


# TODO: add this function to bom_utils
def get_data_from_bom(location):
    workbook = openpyxl.load_workbook(location)
    worksheet = workbook.active

    names = [bom_utils.curate_value(cell.value) for cell in
             bom_utils.get_column(worksheet, 'A') if cell.value]

    versions = [bom_utils.curate_value(cell.value) for cell in
                bom_utils.get_column(worksheet, 'B') if cell.value]

    # Make sure these lists contain equal values. In some cases a component
    # may not have a explicit version, so simply adding the (nv) string to
    # that particular component's version cell is required.
    assert len(names) == len(versions)

    return [(name, version) for name, version in zip(names, versions)]


# TODO: add tests
@click.command()
@click.argument('location', type=click.Path(exists=True, readable=True))
@click.argument('destination', type=click.Path(exists=False), required=True)
@click.help_option('-h', '--help')
def cli(location, destination):
    """
    Given an XLSX input file containing two columns: the gem's name in
    the first column and its version in the second column. Retrieve
    metadata from RubyGems.org, including details such as the owner,
    license, and download URL.
    Alternatively, PurlDB can be used to collect the gem's metadata.
    """
    gems = get_data_from_bom(location)
    results = get_gem_metadata(gems)
    output_results(destination, results)
