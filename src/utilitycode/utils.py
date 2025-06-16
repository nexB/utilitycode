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
import ntpath
import posixpath
import re
import requests

from urllib.parse import urlparse

# https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
import urllib3
urllib3.disable_warnings()


def to_posix(path):
    """
    Return a path using the posix path separator given a path that may contain
    posix or windows separators, converting "\\" to "/". NB: this path will
    still be valid in the windows explorer (except for a UNC or share name). It
    will be a valid path everywhere in Python. It will not be valid for windows
    command line operations.
    """
    return path.replace(ntpath.sep, posixpath.sep)


def get_validity(input):
    """
    Return True if a given string is a valid URI.
    """
    return urlparse(input)


def get_status(input):
    """
    Return the status of URL ('not a URL', 'not-working' and 'working').
    """
    try:
        if get_validity(input):
            r = requests.head(input.strip(), verify=False)
            if r.status_code in [404, 500, 501, 502, 503, 504, 405, 408, 410]:
                return 'not-working'
            else:
                return 'working'
        else:
            return 'not a URL'
    except Exception as e:
        print(str(e))
        return 'not-working'


def validate_url(url):
    """
    Return True if URL is accessible, False otherwise
    """
    if urlparse(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except:
            return False
    return False


def report_errors(errors, quiet, log_file_loc=None):
    """
    Report and save the error message (default: error.log)

    The error will be saved at the `log_file_loc` if it's provided, otherwise,
    it will save at the error.log at the destination directory.
    """
    if errors:
        for error in errors:
            if not quiet:
                click.echo(error)
        with io.open(log_file_loc, 'w', encoding='utf-8', errors='replace') as lf:
            lf.write('\n'.join(errors))
        click.echo("Error log: " + log_file_loc)


def get_owner_repo_from_github_link(github_link):
    """
    Get the owner and repo data from a github link
    """
    pattern = r"github\.com/([^/]+)/([^/]+)"
    match = re.search(pattern, github_link)

    if match:
        owner = match.group(1)
        repo = match.group(2)
        return owner, repo

    return None, None


def get_github_license(owner, repo):
    """
    Get the licesne from github API
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    """
    Use Authenticated requests
    headers = {
        'Authorization': 'Token YOUR_PERSONAL_ACCESS_TOKEN'
    }
    """
    license_key = ''
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            license_key = data.get("license", {}).get("key")
        else:
            return "Failed to fetch repository information."
    except requests.exceptions.ConnectionError as e:
        import time
        print("Max retries exceeded. The tool will resume after 3 minutes.")
        time.sleep(180)
        license_key = get_github_license(owner, repo)
    return license_key


def get_go_package_license(project_link):
    """
    Get the license from pkg.go.dev with web scrapping.
    """
    url = f"https://pkg.go.dev/{project_link}"
    license = ''
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            lines = html_content.splitlines()
            for line in lines:
                if line.strip().startswith('aria-label="Go to Licenses" data-gtmc="header link">'):
                    license = line.partition(
                        'aria-label="Go to Licenses" data-gtmc="header link">')[2].partition('</a')[0]
                elif 'aria-describedby="license-description">' in line:
                    license = line.partition(
                        'aria-describedby="license-description">')[2].partition('</a')[0]
        else:
            license = f"Failed to retrieve package details: {response.status_code}"
    except requests.exceptions.ConnectionError as e:
        import time
        print("Max retries exceeded. The tool will resume after 3 minutes.")
        time.sleep(180)
        license = get_go_package_license(project_link)
    return license


def get_pub_info(package_name, version):
    """
    Get the package's description and repository url from the pub.dev API
    Unfortunately, there is no license and copyright info
    """
    api_url = f"https://pub.dev/api/packages/{package_name}"
    description = ''
    homepage_url = ''
    download_url = ''
    author = ''
    sha256 = ''
    released_date = ''
    data_dict = {}
    try:
        response = requests.get(api_url)
        package_data = response.json()
        # Verify the existance of the package or otherwise return an empty
        # dictionary
        if 'name' in package_data:
            package_version_list = package_data['versions']
            for package_version in package_version_list:
                if package_version['version'] == version:

                    if 'description' in package_version['pubspec']:
                        description = package_version['pubspec']['description']
                    if 'repository' in package_version['pubspec']:
                        homepage_url = package_version['pubspec']['repository']
                    elif 'homepage' in package_version['pubspec']:
                        homepage_url = package_version['pubspec']['homepage']
                    if 'author' in package_version['pubspec']:
                        author = package_version['pubspec']['author']
                    if 'archive_url' in package_version:
                        download_url = package_version['archive_url']
                    if 'archive_sha256' in package_version:
                        sha256 = package_version['archive_sha256']
                    if 'published' in package_version:
                        released_date = package_version['published']

                    data_dict['package__description'] = description
                    data_dict['package__homepage_url'] = homepage_url
                    data_dict['package__download_url'] = download_url
                    data_dict['package__owner'] = author
                    data_dict['package__sha256'] = sha256
                    data_dict['package__release_date'] = released_date
    except requests.exceptions.ConnectionError as e:
        import time
        print("Max retries exceeded. The tool will resume after 3 minutes.")
        time.sleep(180)
        data_dict = get_pub_info(package_name, version)
    return data_dict


def get_pub_package_license(package_name):
    """
    Obtain license information from https://pub.dev/packages/ through web
    scraping
    """
    url = f"https://pub.dev/packages/{package_name}"
    license = ''
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            lines = html_content.splitlines()
            for line in lines:
                if 'title">License' in line:
                    license = line.partition(
                        'title">License')[2].partition(' (<a href="')[0].rpartition('"/>')[2].strip()
                    break
        else:
            license = f"Failed to retrieve package details: {response.status_code}"
    except requests.exceptions.ConnectionError as e:
        import time
        print("Max retries exceeded. The tool will resume after 3 minutes.")
        time.sleep(180)
        license = get_pub_package_license(package_name)
    return license


def get_podfile_info(package_name):
    """
    Get the podfile's package info from https://cocoapods.org/ through web
    scraping
    """
    url = f"https://cocoapods.org/pods/{package_name}"
    info_dict = {}
    try:
        response = requests.get(url)
        if response.status_code == 200:
            homepage_url = False
            is_lang_line = False
            language = False
            license = False
            maintained_by = False

            html_content = response.text
            lines = html_content.splitlines()
            for line in lines:
                if is_lang_line:
                    info_dict['package__primary_language'] = line.rpartition(
                        '<span class="visible-lg-span">')[2].partition('</span>')[0]
                    is_lang_line = False
                    language = True
                elif '<span class="visible-lg-span">Language</span>' in line:
                    is_lang_line = True
                elif '<td>License</td>' in line:
                    if "'>" in line:
                        info_dict['package__declared_license'] = line.rpartition("'>")[
                            2].partition('</a>')[0]
                    else:
                        info_dict['package__declared_license'] = line.rpartition('">')[
                            2].partition('</a>')[0]
                    license = True
                elif 'GitHub Repo' in line and not homepage_url:
                    info_dict['package__homepage_url'] = line.partition('">GitHub Repo')[
                        0].rpartition('a href="')[2]
                    homepage_url = True
                elif '<p>Maintained by' in line:
                    maintainers = line.partition('<p>Maintained by')[
                        2].partition('.</p')[0].strip()
                    maintainers_link_list = maintainers.split('>,')
                    maintainers_list = []
                    for maintainer_link in maintainers_link_list:
                        maintainers_list.append(
                            remove_href_link(maintainer_link))
                    info_dict['package__copyright'] = ', '.join(
                        maintainers_list)
                    maintained_by = True
                if language and maintained_by and homepage_url and license:
                    break
    except requests.exceptions.ConnectionError as e:
        import time
        print("Max retries exceeded. The tool will resume after 3 minutes.")
        time.sleep(180)
        info_dict = get_podfile_info(package_name)
    return info_dict


def remove_href_link(link):
    """
    input: <a href="/owners/13">John Doo</a>
    Return: John Doo
    """
    if "'>" in link:
        return link.partition("'>")[2].partition('</a')[0]
    return link.partition('">')[2].partition('</a')[0]


def get_pypi_info(package_name, version, resource):
    """
    Get the pypi package information from
    https://pypi.org/pypi/{package_name}/{version}/json
    Return a dictionary with the package information
    """
    api_url = f"https://pypi.org/pypi/{package_name}/{version}/json"

    author = ''
    download_url = ''
    home_page = ''
    license = ''
    project_url = ''

    data_dict = {}

    try:
        response = requests.get(api_url)
        data_dict['Resource'] = resource
        data_dict['package__type'] = 'pypi'
        data_dict['package__name'] = package_name
        data_dict['package__version'] = 'v ' + version
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            package_data = response.json()
            if 'info' in package_data:
                package_info_dict = package_data['info']
                if 'author' in package_info_dict:
                    author = package_info_dict['author']
                if 'download_url' in package_info_dict:
                    download_url = package_info_dict['download_url']
                if 'home_page' in package_info_dict:
                    home_page = package_info_dict['home_page']
                if 'license' in package_info_dict:
                    license = package_info_dict['license']
                if 'project_url' in package_info_dict:
                    project_url = package_info_dict['project_url']
                if home_page:
                    data_dict['package__homepage_url'] = home_page
                else:
                    data_dict['package__homepage_url'] = project_url
                data_dict['package__download_url'] = download_url
                data_dict['package__owner'] = author
                data_dict['package__declared_license'] = license
    except requests.exceptions.ConnectionError as e:
        import time
        print("Max retries exceeded. The tool will resume after 3 minutes.")
        time.sleep(180)
        data_dict = get_pypi_info(package_name, version, resource)
    return data_dict
