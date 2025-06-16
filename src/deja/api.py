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

from urllib.parse import quote
from urllib.parse import urlencode
from urllib.request import Request
from urllib.request import urlopen
from urllib.error import HTTPError

import requests
import json
import urllib.request


HOST_owners = 'https://enterprise.dejacode.com/api/v2/owners/'
HOST_packages = 'https://enterprise.dejacode.com/api/v2/packages/'
HOST_components = 'https://enterprise.dejacode.com/api/v2/components/'
SCANCODE_LICENSEDB = 'https://scancode-licensedb.aboutcode.org/'

VERSION = '0.0.2'


def get_package_by_download_url(download_url, api_key):
    '''
    Given a package's download_url, return the package from dejacode
    '''
    headers = {
        'Authorization': 'Token {}'.format(api_key),
        'Accept': 'application/json; indent=4',
    }

    payload = {'download_url': download_url}
    response = requests.get(HOST_packages, headers=headers, params=payload)
    if response.status_code == requests.codes.ok:
        return response.json().get('results')[0]


def get_component_name_versions(name_versions, dje_api_key):
    '''
    Given a list of component name:versions, return a list of component name:versions
    that are missing from DJE. Also, print out a component changelist URL for easy
    copying of existing components to a new dataspace.
    '''
    headers = {
        'Authorization': 'Token {}'.format(dje_api_key),
        'Accept': 'application/json; indent=4',
    }
    # mass-query the component_versions
    results = []
    chunks = [name_versions[x:x+100]
              for x in xrange(0, len(name_versions), 100)]
    for chunk in chunks:
        payload = {'page_size': 100, 'reference': 1,
                   'name_version': name_versions}
        response = requests.get(
            HOST_components, headers=headers, params=payload)
        if response.status_code == requests.codes.ok:
            results.extend(response.json().get('results'))

    return results


def get_licenses_dje(license_key, api_url, api_key):
    """
    Return a tuple of (dictionary of license data, list of errors) given a
    `license_key`. Send a request to `api_url` authenticating with `api_key`.
    """
    headers = {
        'Authorization': 'Token %s' % api_key,
    }
    payload = {
        'api_key': api_key,
        'key': license_key,
        'format': 'json'
    }

    api_url = api_url.rstrip('/')
    payload = urlencode(payload)

    full_url = '%(api_url)s/?%(payload)s' % locals()
    # handle special characters in URL such as space etc.
    quoted_url = quote(full_url, safe="%/:=&?~#+!$,;'@()*[]")

    license_data = {}
    error = ''
    try:
        request = Request(quoted_url, headers=headers)
        response = urlopen(request)
        response_content = response.read().decode('utf-8')
        license_data = json.loads(response_content)
        if not license_data.get('results', []):
            error = u"Invalid 'license': %s" % license_key
    except HTTPError as http_e:
        error = u"Authorization denied. Invalid '--api_key'."
    except Exception as e:
        # Already checked the authorization and accessible of the URL.
        # The only exception left is URL is accessible, but it's not a valid API URL
        error = u"Invalid '--api_url'."

    finally:
        if license_data.get('count') == 1:
            license_data = license_data.get('results')[0]
        else:
            license_data = {}

    return license_data, error


def get_licenses_licensedb(license_keys):
    results = []
    errors = []
    for key in license_keys:
        link = SCANCODE_LICENSEDB + key + '.json'
        try:
            with urllib.request.urlopen(link) as url:
                value = url.read()
                dict = json.loads(value.decode('utf-8'))
                # Since the LicenseDB doesn't provide the License URL, we will just
                # create one
                dict['absolute_url'] = SCANCODE_LICENSEDB + key + '.LICENSE'
                results.append(dict)
        except:
            error = u"Invalid 'license': %s" % key
            errors.append(error)

    return results, errors


def get_owners(owners, dje_api_key):
    '''
    Given a list of owner names, query DejaCode for these owners and return the
    API results.
    '''
    headers = {
        'Authorization': 'Token {}'.format(dje_api_key),
        'Accept': 'application/json; indent=4',
    }

    results = []
    chunks = [owners[x:x+100] for x in xrange(0, len(owners), 100)]
    for chunk in chunks:
        payload = {'page_size': 100, 'reference': 1, 'name': owners}
        response = requests.get(HOST_owners, headers=headers, params=payload)
        if response.status_code is requests.codes.ok:
            results.extend(response.json().get('results'))

    return results


def get_owner_url(owner_name, api_key):
    '''
    Given an owner name, return the DejaCode api_url for that particular owner.
    '''
    headers = {
        'Authorization': 'Token {}'.format(api_key),
        'Accept': 'application/json; indent=4',
    }
    params = {'name': owner_name}
    response = requests.get(HOST_owners, headers=headers, params=params)
    if response.status_code == requests.codes.ok:
        result = response.json().get('results')

    return result[0].get('api_url')
