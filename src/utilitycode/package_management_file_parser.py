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

from collections import OrderedDict
import json

from packagedcode import npm
from packagedcode.gemfile_lock import GemfileLockParser
from formattedcode import output_csv

import click
import csv
import os
import requests
import yaml

from utilitycode.bom_utils import write_to_csv, write_to_xlsx
from utilitycode.utils import get_go_package_license
from utilitycode.utils import get_owner_repo_from_github_link
from utilitycode.utils import get_podfile_info
from utilitycode.utils import get_pub_info
from utilitycode.utils import get_pub_package_license
from utilitycode.utils import get_pypi_info

output_headers = [
    'path',
    'package__type',
    'package__namespace',
    'package__name',
    'package__version',
    'package__qualifiers',
    'package__subpath',
    'package__primary_language',
    'package__description',
    'package__release_date',
    'package__homepage_url',
    'package__download_url',
    'package__size',
    'package__sha1',
    'package__md5',
    'package__sha256',
    'package__sha512',
    'package__bug_tracking_url',
    'package__code_view_url',
    'package__vcs_url',
    'package__copyright',
    'package__license_expression',
    'package__declared_license',
    'package__notice_text',
    'package__root_path',
    'package__contains_source_code',
    'package__extra_data',
    'package__purl',
    'package__source_location'
]


class LockPackage():
    def __init__(self, name='', version='', dev=False):
        self.name = name
        self.version = version
        self.license = ''
        self.description = ''
        self.dev = dev
        self.tk_package = ''

    def api_url_glock(self):
        return 'https://rubygems.org/api/v2/rubygems/{}/versions/{}.json'.format(self.name, self.version)

    def api_url_plock(self):
        return 'https://registry.npmjs.org/{}/{}'.format(self.name, self.version)

    def api_url_ylock(self):
        return 'https://registry.npmjs.org/{}/'.format(self.name)

    def get_version(self):
        return 'v {}'.format(self.version)

    def gem_download_url(self):
        return 'https://rubygems.org/downloads/{}-{}.gem'.format(self.name, self.version)

    def homepage_url(self):
        return 'https://rubygems.org/gems/{}/versions/{}'.format(self.name, self.version)

    def to_dict(self):
        return OrderedDict([
            ('package__name', self.name),
            ('package__version', self.get_version()),
            ('package__declared_license', self.license),
            ('package__description', self.description),
            ('package__download_url', self.gem_download_url()),
            ('package__homepage_url', self.homepage_url())
        ])


def create_glock_packages(gfl):
    for gem in gfl.all_gems:
        yield LockPackage(gfl.all_gems[gem].name, gfl.all_gems[gem].version)


def create_plock_packages(deps):
    """
    Given a package-lock.json depenencies dictionary, yield LockPackage
    objects.
    """
    for name, info in deps.items():
        version, dev = info.get('version', ''), info.get('dev', False)
        yield LockPackage(name=name, version=version, dev=dev)


def create_ylock_packages(ylock_list):
    """
    Given a name and version parsed from yarn.lock file, yield LockPackage
    objects.
    """
    for name, version in ylock_list:
        yield LockPackage(name=name, version=version)


def extract_go_sum_data(gosum):
    """
    Extract the link, version, owner and repo from the go.sum file.
    """
    gosum_package_list = []
    errors = []
    try:
        # Get the project link and version from go.sum
        with open(gosum, 'r') as go_file:
            reader = csv.reader(go_file, delimiter=' ')
            for row in reader:
                # Only get the one that has 'go.mod' in the version column
                if row[1].endswith('go.mod'):
                    package_dict = {}
                    package_dict['Resource'] = gosum
                    package_dict['package__homepage_url'] = row[0]
                    version = row[1].partition('/go.mod')[0]
                    # Since the 'v' is attached with the value, we want to
                    # insert a space for consistance
                    package_dict['package__version'] = version[:1] + \
                        " " + version[1:]
                    if row[0].startswith('github'):
                        package_dict['package__owner'], package_dict['package__name'] = get_owner_repo_from_github_link(
                            row[0])
                    else:
                        # Use the last segment of the link as the package__name
                        package_dict['package__name'] = row[0].rpartition(
                            '/')[2]
                        package_dict['package__owner'] = ''
                    gosum_package_list.append(package_dict)
    except FileNotFoundError:
        error_msg = "File not found: " + gosum
        errors.append(error_msg)
    except IOError:
        error_msg = "Error reading the file." + gosum
        errors.append(error_msg)
    return gosum_package_list, errors


def parse_go_mod(gomod):
    gomod_package_list = []

    with open(gomod, 'r') as file:
        lines = file.readlines()
        package_line = False
        capture_notes = False
        for line in lines:
            package_dict = {}
            line = line.strip()
            if line.startswith(')'):
                package_line = False
                capture_notes = False
            elif line.startswith('require'):
                package_line = True
            elif package_line:
                if line.endswith('indirect'):
                    package_dict['notes'] = 'Indirect dependency'
                row = line.split(' ')
                url = row[0]
                version = row[1]
                package_dict['package__homepage_url'] = url
                if version.startswith('v'):
                    package_dict['package__version'] = 'v ' + \
                        version.partition('v')[2]
                else:
                    package_dict['package__version'] = 'v ' + version
                if url.startswith('github'):
                    package_dict['package__owner'], package_dict['package__name'] = get_owner_repo_from_github_link(
                        url)
                else:
                    # Use the last segment of the link as the package__name
                    package_dict['package__name'] = url.rpartition(
                        '/')[2]
                    package_dict['package__owner'] = ''
            elif line.startswith('replace'):
                capture_notes = True
            elif capture_notes:
                package_dict['notes'] = 'Replace: ' + line
            if package_dict:
                package_dict['Resource'] = gomod
                gomod_package_list.append(package_dict)
    return gomod_package_list


def extract_pubspec_data(data_dict, pubspec_lock):
    """
    Extract the data from the pubspec.lock and fetch license
    """
    packages_list = []
    for package in data_dict['packages']:
        package_dict = {}
        version = data_dict['packages'][package]['version']
        package_dict['Resource'] = pubspec_lock
        package_dict['package__type'] = 'dart'
        package_dict['package__name'] = package
        package_dict['package__version'] = 'v ' + version
        package_des_url = get_pub_info(package, version)
        package_dict['package__name'] = package
        if package_des_url:
            package_dict.update(package_des_url)
            package_dict['package__declared_license'] = get_pub_package_license(
                package)
        packages_list.append(package_dict)

    return packages_list


def update_gem_data(lock_gems):
    for gem in lock_gems:
        try:
            response = requests.get(gem.api_url_glock())
        except requests.exceptions.ConnectionError:
            import sys
            print(
                "Failed to connect. Please check your internet connection and try again.")
            sys.exit(1)
        if response.status_code != 200:
            continue

        gem_data = response.json()

        license_data = gem_data.get('licenses', '')
        if isinstance(license_data, list):
            gem.license = ','.join(license_data)
        else:
            gem.license = license_data

        gem.description = gem_data.get('description', '')


def update_package_with_data(package, data):
    """
    Update LockPackage object with origin info found in npm api package_data.
    """
    # package.tk_package = npm.build_package(data)
    package.tk_package = npm.NpmPackageJsonHandler._parse(data)


def flatten(package, metafile_location, glock=False, plock=False, ylock=False):
    """
    Yield flattened ScanCode NPM Package for output csv file.
    """
    try:
        if plock:
            response = requests.get(package.api_url_plock())
        if ylock:
            response = requests.get(package.api_url_ylock())
    except requests.exceptions.ConnectionError:
        import sys
        print("Failed to connect. Please check your internet connection and try again.")
        sys.exit(1)
    if not response.status_code == 200:
        data = {'name': package.name, 'version': package.version}
    else:
        if plock:
            data = response.json()
        elif ylock:
            content = response.json()
            try:
                version_data = content['versions']
                data = version_data[package.version]
            except KeyError:
                # Return only the name and version if the specific version
                # cannot be found
                data = {'name': package.name, 'version': package.version}
    # add NPMPackage object to LockPackage objects
    update_package_with_data(package, data)
    package.tk_package.license_expression = package.tk_package.declared_license_expression

    return output_csv.flatten_package(package.tk_package.to_dict(), metafile_location)


def get_ylock_name_version(input):
    """
    Return a list contains name and version information for the packages
    found in the yarn.lock
    """
    with open(input) as f:
        content = f.readlines()
        ylock_name_version_list = []
        name = ''
        version = ''
        for line in content:
            if line.strip():
                if line.startswith('#') or line.startswith('__metadata:'):
                    continue
                if line.startswith(' ') and name:
                    if line.strip().startswith('version'):
                        version = line.partition('version')[
                            2].replace(":", "").replace("\"", "").strip()
                        ylock_name_version_list.append([name, version])
                        continue
                else:
                    comp_list = line.split(" ")
                    name = comp_list[0].strip("\"").rpartition('@')[0]
    return ylock_name_version_list


def get_management_files(input_location, ignore_files=[]):
    """
    Return a list which contains the absolute path for the package management
    files such as Gemfile.lock, package-lock.json, yarn.lock, go.sum,
    pubspec.lock, pipfile.lock
    """
    supported_files = ['package-lock.json', 'gemfile.lock',
                       'yarn.lock', 'go.sum', 'go.mod', 'pubspec.lock',
                       'pipfile.lock', 'requirements.txt', 'podfile.lock',
                       '.control']
    assert input_location
    file_management_list = []

    if os.path.isdir(input_location):
        for root, dirs, files in os.walk(input_location):
            for file in files:
                filepath = os.path.join(root, file)
                if any(filepath.lower().endswith(supported_file) for supported_file in supported_files) and not any(filepath.endswith(ignore_file) for ignore_file in ignore_files):
                    file_management_list.append(filepath)
                else:
                    continue
    else:
        if any(input_location.lower().endswith(supported_file) for supported_file in supported_files) and not any(input_location.endswith(ignore_file) for ignore_file in ignore_files):
            file_management_list.append(input_location)

    return file_management_list


def pubspec_lock_process(pubspec_lock):
    pubspec_lock_package_list = []
    # Open the YAML-formatted pubspec.lock file and load its contents into a
    # dictionary
    with open(pubspec_lock, "r") as lock_file:
        data = yaml.safe_load(lock_file)
        data_list = extract_pubspec_data(data, pubspec_lock)
        pubspec_lock_package_list.extend(data_list)
    return pubspec_lock_package_list


def gosum_process(gosum):
    gosum_package_list = []
    data_list = []
    errors = []
    data_list, err = extract_go_sum_data(gosum)
    handled_project = {}
    if err:
        errors.extend(err)
    for data in data_list:
        data['package__type'] = 'golang'
        project_link = data['package__homepage_url']
        if project_link in handled_project:
            project_license = handled_project[project_link]
        else:
            project_license = get_go_package_license(project_link)
            handled_project[project_link] = project_license
        if not project_link.startswith('http'):
            data['package__homepage_url'] = 'https://' + project_link
        data['package__declared_license'] = project_license
        gosum_package_list.append(data)

    return gosum_package_list, errors


def gomod_process(gomod):
    gomod_package_list = []
    data_list = []
    data_list = parse_go_mod(gomod)

    handled_project = {}

    for data in data_list:
        project_link = ''
        data['package__type'] = 'golang'
        if 'package__homepage_url' in data:
            project_link = data['package__homepage_url']
        if project_link:
            if project_link in handled_project:
                project_license = handled_project[project_link]
            else:
                project_license = get_go_package_license(project_link)
                handled_project[project_link] = project_license
            if not project_link.startswith('http'):
                data['package__homepage_url'] = 'https://' + project_link
            data['package__declared_license'] = project_license
        gomod_package_list.append(data)

    return gomod_package_list


def glock_process(glock_file):
    glock_package_list = []
    gemfile_lock = GemfileLockParser(glock_file)
    lock_gems = list(create_glock_packages(gemfile_lock))
    update_gem_data(lock_gems)
    for gem in lock_gems:
        g_dict = gem.to_dict()
        g_dict['Resource'] = glock_file
        g_dict['package__type'] = 'gem'
        glock_package_list.append(g_dict)
    return glock_package_list


def plock_process(lock_file, no_dev=False):
    plock_package_list = []
    with open(lock_file) as f:
        deps = json.load(f).get('dependencies', {})
    if not deps:
        return plock_package_list
    lock_packages = list(create_plock_packages(deps))

    for package in lock_packages:
        if no_dev:
            if not package.dev:
                plock_package_list.append(
                    flatten(package, lock_file, plock=True))
        else:
            plock_package_list.append(
                flatten(package, lock_file, plock=True))

    return plock_package_list


def ylock_process(lock_file):
    ylock_package_list = []
    ylock_info_list = get_ylock_name_version(lock_file)
    lock_packages = list(create_ylock_packages(ylock_info_list))
    for package in lock_packages:
        ylock_package_list.append(flatten(package, lock_file, ylock=True))
    return ylock_package_list


def pipfile_lock_process(pipfile_lock):
    pipfile_lock_package_list = []
    with open(pipfile_lock) as f:
        data = json.load(f)
    # Extract the default section into a dictionary
    default = data['default']
    for package in default:
        name = package
        version = default[package]['version'].partition('==')[2]
        info_dict = get_pypi_info(name, version, pipfile_lock)
        pipfile_lock_package_list.append(info_dict)
    return pipfile_lock_package_list


def requirements_process(req_file):
    requirements_package_list = []
    with open(req_file, "r") as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            # Ignore empty lines and lines starting with '#'
            if line and not line.startswith("#"):
                package = line.split('==')
                name = package[0]
                version = package[1]
                info_dict = get_pypi_info(name, version, req_file)
                requirements_package_list.append(info_dict)
    return requirements_package_list


def podfile_process(podfile_lock):
    podfile_package_list = []
    in_pod = False
    with open(podfile_lock, "r") as file:
        for line in file:
            stripped_line = line.strip()
            if in_pod:
                if stripped_line == 'DEPENDENCIES:' or stripped_line == 'EXTERNAL SOURCES:' or stripped_line == 'SPEC CHECKSUMS:' or stripped_line == 'PODFILE CHECKSUM:':
                    break
                if line.startswith('  - '):
                    info_dict = {}
                    package_name = line.partition(
                        '  - ')[2].partition(' (')[0].strip()
                    package_version = line.partition(
                        ' (')[2].partition(')')[0].strip()
                    info_dict['Resource'] = podfile_lock
                    info_dict['package__type'] = 'cocoapods'
                    info_dict['package__name'] = package_name
                    info_dict['package__version'] = 'v ' + package_version
                    info_dict.update(get_podfile_info(package_name))
                    podfile_package_list.append(info_dict)
            if stripped_line == 'PODS:':
                in_pod = True

    return podfile_package_list


def opk_contol_file_process(control_file):
    info_dict = {}
    with open(control_file, "r") as file:
        info_dict['Resource'] = control_file
        info_dict['package__type'] = 'OpenWRT'
        previous_field = ''
        for line in file:
            if line:
                if not line.startswith(' '):
                    previous_field = ''
                    key = line.partition(':')[0].strip()
                    value = line.partition(':')[2].strip()
                    if key == 'Package':
                        field = 'package__name'
                    elif key == 'Version':
                        field = 'package__version'
                    elif key == 'Source':
                        field = 'package__source_location'
                    elif key == 'License':
                        field = 'package__declared_license'
                    elif key == 'LicenseFiles':
                        field = 'package__notice_text'
                    elif key == 'RemoteUrl':
                        field = 'package__homepage_url'
                    elif key == 'Maintainer':
                        field = 'package__copyright'
                    elif key == 'Installed-Size':
                        field = 'package__size'
                    elif key == 'Description':
                        field = 'package__description'
                    else:
                        continue
                    if field == 'package__version':
                        info_dict[field] = 'v ' + value
                    else:
                        info_dict[field] = value
                    previous_field = field
                else:
                    info_dict[previous_field] = info_dict[previous_field] + \
                        ' ' + line.strip()
    return [info_dict]


@click.command()
@click.option('--csv',
              is_flag=True,
              help='Output as CSV format (Default: XLSX format)')
@click.option('--ignore', multiple=True, help='File to be ignored.')
@click.option('--no-dev',
              is_flag=True,
              help='Exclude dependencies that have ["dev": true] in package-lock.json')
@click.argument('input_location', type=click.Path(exists=True, readable=True))
@click.argument('output', type=click.Path(exists=False), required=True)
@click.help_option('-h', '--help')
def cli(csv, ignore, no_dev, input_location, output):
    """
    Recursively parse the package management files from the
    input location and output the parsed data.

    \b
    Supported files:
     - Gemfile.lock
     - package-lock.json
     - yarn.lock
     - go.mod
     - go.sum
     - pubspec.lock
     - Pipfile.lock
     - requirements.txt
     - Podfile.lock
     - *.control
    """
    metadata_list = []
    ignore_files = []
    if ignore:
        ignore_files = list(ignore)
    # Order the output headers
    header_dict = {}
    for header in output_headers:
        header_dict[header] = None
    metadata_list.append(header_dict)

    management_files_list = get_management_files(input_location, ignore_files)

    for management_file in management_files_list:
        print("Working on: " + management_file)
        if management_file.lower().endswith('package-lock.json'):
            plock_package_list = plock_process(management_file, no_dev)
            for ppackage in plock_package_list:
                metadata_list.append(ppackage)
        elif management_file.lower().endswith('gemfile.lock'):
            glock_package_list = glock_process(management_file)
            for gpackage in glock_package_list:
                metadata_list.append(gpackage)
        elif management_file.lower().endswith('yarn.lock'):
            ylock_package_list = ylock_process(management_file)
            for ypackage in ylock_package_list:
                metadata_list.append(ypackage)
        elif management_file.lower().endswith('go.sum'):
            gosum_package_list, errors = gosum_process(management_file)
            if errors:
                print(errors)
            for gopackage in gosum_package_list:
                metadata_list.append(gopackage)
        elif management_file.lower().endswith('go.mod'):
            gomod_package_list = gomod_process(management_file)
            for gopackage in gomod_package_list:
                metadata_list.append(gopackage)
        elif management_file.lower().endswith('pubspec.lock'):
            pubspec_lock_package_list = pubspec_lock_process(
                management_file)
            for pubspec_lock_package in pubspec_lock_package_list:
                metadata_list.append(pubspec_lock_package)
        elif management_file.lower().endswith('pipfile.lock'):
            pipfile_lock_package_list = pipfile_lock_process(management_file)
            for pipfile_lock_package in pipfile_lock_package_list:
                metadata_list.append(pipfile_lock_package)
        elif management_file.lower().endswith('requirements.txt'):
            requirements_package_list = requirements_process(management_file)
            for requirements_package in requirements_package_list:
                metadata_list.append(requirements_package)
        elif management_file.lower().endswith('podfile.lock'):
            podfile_package_list = podfile_process(management_file)
            for podfile_package in podfile_package_list:
                metadata_list.append(podfile_package)
        elif management_file.lower().endswith('.control'):
            opk_contol_file_list = opk_contol_file_process(management_file)
            for opk_contol_file in opk_contol_file_list:
                metadata_list.append(opk_contol_file)

    if csv:
        if not output.endswith('.csv'):
            raise click.UsageError(
                'ERROR: "The output does not ends with \'.csv\' extension.')
        else:
            write_to_csv(metadata_list, output)
    else:
        if not output.endswith('.xlsx'):
            raise click.UsageError(
                'ERROR: "The output does not ends with \'.xlsx\' extension.')
        else:
            write_to_xlsx(metadata_list, output)

    print("\nFinished!")
