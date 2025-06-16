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
import copy
import requests
import json
import packageurl

from urllib.request import urlopen

from spreadsheet_toolkit.csv_utils import read_csv_rows
from packagedcode import npm
from formattedcode import output_csv

from utilitycode.bom_utils import get_data_from_xlsx
from utilitycode.bom_utils import write_to_csv
from utilitycode.bom_utils import write_to_xlsx


PACKAGE_FIELDS = ['package__type', 'package__namespace', 'package__name',
                  'package__version', 'package__qualifiers',
                  'package__subpath', 'package__primary_language',
                  'package__description', 'package__release_date',
                  'package__homepage_url', 'package__download_url',
                  'package__size', 'package__sha1', 'package__md5',
                  'package__sha256', 'package__sha512',
                  'package__bug_tracking_url', 'package__code_view_url',
                  'package__vcs_url', 'package__copyright',
                  'package__license_expression', 'package__declared_license',
                  'package__notice_text', 'package__root_path',
                  'package__contains_source_code', 'package__extra_data',
                  'package__purl']


class Package():
    def __init__(self, name='', version='', dev=False):
        self.name = name
        self.version = version
        self.dev = dev
        self.tk_package = ''

    def api_url(self):
        return 'https://registry.npmjs.org/{}/'.format(self.name)

    def to_dict(self):
        return dict([
            ('name', self.name),
            ('version', self.version),
        ])


def get_name_version_from_json(input):
    """
    Return a list contains name and version information for the npm packages
    found in the purl field from an json input.
    """
    packages_name_version_list = []
    err_msg = ''
    with open(input) as f:
        deps = json.load(f).get('files', {})
        # This is written for the compatibility for all "older" version of
        # scancode-toolkit
        package_field_list = ['packages', 'package_manifests', 'package_data']
        package_field_name = None
        for dep in deps:
            if package_field_name:
                break
            for key in package_field_list:
                if dep.get(key):
                    package_field_name = key
                    break
        if not package_field_name:
            err_msg = 'The input does not have the package information.'
            return packages_name_version_list, err_msg
        for dep in deps:
            packages = dep.get(package_field_name, {})
            for p in packages:
                npm_name = ""
                npm_version = ""
                purl = p['purl']
                if purl and p['type'] == 'npm':
                    npm_name, npm_version = get_name_version_from_purl(purl)
                if npm_name:
                    packages_name_version_list.append((npm_name, npm_version))
    return packages_name_version_list, err_msg


def fetch_process(result, purl_field_name):
    """
    Return a list of dictionary that contains the original data and the fetched
    package information from the purl field.
    """
    updated_rows = []
    err_msg = ''
    for row in result:
        if purl_field_name not in row:
            err_msg = "'purl' field is not found in the input."
            return updated_rows, err_msg
        row_dict = copy.deepcopy(row)
        package_dict = {}
        npm_name = ""
        npm_version = ""
        purl = row[purl_field_name]
        if purl:
            if purl.startswith('pkg:npm/'):
                print("Working on: " + purl)
                npm_name, npm_version = get_name_version_from_purl(purl)
                package_dict = flatten(
                    Package(name=npm_name, version=npm_version))
                # Fetch extra information
                fetched_dict = fetch_information(npm_name, npm_version)
                package_dict['package__author'] = fetched_dict['package__author']
                package_dict['package_contributors'] = fetched_dict['package_contributors']
                if not package_dict['package__homepage_url'] and fetched_dict['package__homepage_url']:
                    package_dict['package__homepage_url'] = fetched_dict['package__homepage_url']
                if not package_dict['package__version']:
                    # The 'package_download_url' is incorrect if the purl doesn't have version
                    # i.e. it will be something like: https://registry.npmjs.org/<package>/-/<name>-None.tgz
                    # which is invalid
                    package_dict['package__download_url'] = fetched_dict['package__download_url']
                if not package_dict['package__declared_license_expression'] and fetched_dict['package__declared_license']:
                    package_dict['package__declared_license_expression'] = fetched_dict['package__declared_license']

        if package_dict:
            for package_item in package_dict:
                row_dict[package_item] = package_dict[package_item]
        else:
            for package_field in PACKAGE_FIELDS:
                row_dict[package_field] = ""
        updated_rows.append(row_dict)
    return updated_rows, err_msg


def fetch_information(npm_name, npm_version):
    """
    This utility will fetch information from https://registry.npmjs.org/
    """
    base_link = 'https://registry.npmjs.org/'
    link = base_link + npm_name
    """
    We want name, version, homepage, author and license information
    """
    package_author = ''
    package_contributors = ''
    package_homepage = ''
    package_lic = ''
    package_download_url = ''
    npm_dict = {}
    try:
        f = urlopen(link)
        print(link)
        content = f.read()

        res = json.loads(content)
        if not npm_version:
            all_versions = res['versions']
            # Get the first version in the registry.npmjs.org
            version = list(all_versions.keys())[0]
        else:
            version = npm_version
        try:
            package_author = res['versions'][version]['author']['name']
        except:
            pass
        try:
            package_homepage = res['versions'][version]['homepage']
        except:
            pass
        try:
            contributors_list = res['versions'][version]['contributors']
            for contributor in contributors_list:
                package_contributors += contributor['name'] + '\n'
            package_contributors = package_contributors.strip()
        except:
            pass
        try:
            package_download_url = res['versions'][version]['dist']['tarball']
        except:
            pass
        try:
            if 'license' in res['versions'][version]:
                package_lic = res['versions'][version]['license']
            elif 'licenses' in res['versions'][version]:
                package_lic = res['versions'][version]['licenses']
            elif 'license' in res:
                package_lic = res['license']
        except:
            pass
    except:
        pass

    npm_dict['package__author'] = str(package_author)
    npm_dict['package__homepage_url'] = str(package_homepage)
    npm_dict['package__declared_license'] = str(package_lic)
    npm_dict['package__download_url'] = str(package_download_url)
    npm_dict['package_contributors'] = str(package_contributors)
    return npm_dict


def get_name_version_from_purl(purl):
    """
    Return npm_name and npm_version parsed from the purl.
    """
    try:
        purl = packageurl.PackageURL.from_string(purl)
        if purl.namespace:
            npm_name = purl.namespace + '/' + purl.name
        else:
            npm_name = purl.name
        npm_version = purl.version
    except:
        # else:
        # Handle case that purl does not have version data
        npm_name = purl.partition('pkg:npm/')[2]
        npm_version = ''
    return npm_name, npm_version


def create_packages(package_list):
    """
    Given a name and version parsed from the purl, yield Package objects.
    """
    for name, version in package_list:
        yield Package(name=name, version=version)


def update_package_with_data(package, data):
    """
    Update Package object with origin info found in npm api package_data.
    """
    # package.tk_package = npm.build_package(data)
    package.tk_package = npm.NpmPackageJsonHandler._parse(data)


def flatten(package):
    """
    Return a dictionary of flattened ScanCode NPM Package information
    """
    response = requests.get(package.api_url())
    if not response.status_code == 200:
        data = {'name': package.name, 'version': package.version}
    else:
        content = response.json()
        try:
            version_data = content['versions']
            data = version_data[package.version]
        except:
            # Return a simple name and version dictionary if the package
            # version is not found in content
            data = {'name': package.name, 'version': package.version}

    # add NPMPackage object to Package objects
    update_package_with_data(package, data)
    package.tk_package.license_expression = package.tk_package.declared_license_expression
    package_dict = {}
    metafile_location = ''
    # The "flatten_package" needs the metafile location which we don't need
    # it ('Resource') So, we will remove it from the dictionary
    package_dict = output_csv.flatten_package(
        package.tk_package.to_dict(), metafile_location)
    if 'Resource' in package_dict:
        del package_dict['Resource']
    return package_dict


def download_packages(packages_list, destination):
    """
    Download the packages to the user defined destination.
    """
    import requests
    downloaded_package = []
    for package in packages_list:
        url = package['package__download_url']
        if url:
            if url in downloaded_package:
                continue
            downloaded_package.append(url)
            name = package['package__name']
            version = package['package__version'].partition('v ')[2]
            response = requests.get(url)
            if response.status_code == requests.codes.ok:
                with open('{}/{}-{}.tar.gz'.format(destination, name, version), 'wb') as pkg:
                    pkg.write(response.content)


@click.command()
@click.option('--scancode',
              is_flag=True,
              help='Indicate the input file is generated from scancode_toolkit.')
@click.option('--download',
              metavar='DIR',
              type=click.Path(exists=True, file_okay=False,
                              readable=True, resolve_path=True),
              help='Path to a directory where the package should be downloaded to.')
@click.option('--csv',
              is_flag=True,
              help='Output as CSV format (Default: XLSX format)')
@click.argument('input', type=click.Path(exists=True, readable=True), required=True)
@click.argument('output', type=click.Path(exists=False), required=True)
@click.help_option('-h', '--help')
def cli(scancode, download, csv, input, output):
    '''
    Get the package information from 'https://registry.npmjs.org/' with the
    purl field in the input file.
    The input can be generated from Scancode Toolkit (JSON/CSV) or
    custom (CSV/XLSX).
    The output has to be either .csv or .xlsx
    '''
    if not output.endswith('.csv') and not output.endswith('.xlsx'):
        raise click.UsageError(
            'ERROR: Invalid output file extension: must be .csv or .xlsx.')
    if scancode:
        if not input.endswith(('.csv', '.json',)):
            raise click.UsageError(
                'ERROR: Invalid input file extension: must be .csv or .json.')
    else:
        if not input.endswith(('.csv', '.xlsx',)):
            raise click.UsageError(
                'ERROR: Invalid non-scancode toolkit input file. Extension must be .csv or .xlsx.')

    flattened_packages = []
    packages_name_version_list = []
    err = ""
    # This is to handle the JSON file input from scancode-tk
    if input.endswith('.json'):
        packages_name_version_list, err = get_name_version_from_json(input)
        if err:
            raise click.UsageError(err)
        if not packages_name_version_list:
            print("No NPM package detected in the input.")
        else:
            packages = list(create_packages(packages_name_version_list))
            for package in packages:
                flattened_packages.append(flatten(package))
    else:
        purl_field_name = 'purl'
        if input.endswith('.csv'):
            if scancode:
                purl_field_name = 'package__purl'
            result = read_csv_rows(input)
        else:
            result, _header = get_data_from_xlsx(input)
        flattened_packages, err = fetch_process(result, purl_field_name)
        if err:
            raise click.UsageError(err)

    if download:
        download_packages(flattened_packages, download)

    if csv:
        write_to_csv(flattened_packages, output)
    else:
        write_to_xlsx(flattened_packages, output)
