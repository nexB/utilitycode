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

from openpyxl import load_workbook
from license_expression import Licensing

from deja import api
from utilitycode import bom_utils, utils


def get_license_data(license_keys, api_url, api_key):
    """
    Given a list of license keys, query the Dejacode API to retrive license data.
    Return a list of license_appendix_entries, which are tuples containing the
    wanted license information from DejaCode.
    """
    fatal_errors = [
        "Authorization denied. Invalid '--api_key'.",  "Invalid '--api_url'."]
    errors = []
    license_appendix_entries = []
    if api_url:
        results = []
        for lic_key in license_keys:
            lic_data, error = api.get_licenses_dje(lic_key, api_url, api_key)
            if error:
                errors.append(error)
                if error in fatal_errors:
                    return license_appendix_entries, errors
            if lic_data:
                results.append(lic_data)
    else:
        results, errors = api.get_licenses_licensedb(license_keys)

    for result in results:
        license_appendix_entry = [
            result.get('key'),
            result.get('spdx_license_key'),
            result.get('category'),
            result.get('absolute_url'),
        ]
        license_appendix_entries.append(license_appendix_entry)

    return license_appendix_entries, errors


@click.command()
@click.argument('expression_column_name')
@click.argument('location', type=click.Path(exists=True, readable=True))
@click.argument('destination', type=click.Path(exists=False), required=True)
@click.option('--api_url',
              nargs=1,
              type=click.STRING,
              metavar='URL',
              help='URL to DejaCode License Library.')
@click.option('--api_key',
              nargs=1,
              type=click.STRING,
              metavar='KEY',
              help='API Key for the DejaCode License Library')
def cli(expression_column_name, location, destination, api_url, api_key):
    """
    This utility will generate the "SPDX Short Identifier", "ScanCode
    License Category" and "ScanCode License URL" based on the license
    expression value. If no API information is provided, the tool will use
    data from ScanCode LicenseDB.
    """
    # Check if both api_url and api_key present
    if api_url or api_key:
        if not api_url:
            msg = '"--api_url" is required.'
            click.echo(msg)
            sys.exit(1)
        if not api_key:
            msg = '"--api_key" is required.'
            click.echo(msg)
            sys.exit(1)
    else:
        api_url = ''
        api_key = ''
    api_url = api_url.strip("'").strip('"')
    api_key = api_key.strip("'").strip('"')

    input_bom = load_workbook(location)
    input_ws = input_bom.active
    header_dict = bom_utils.get_header_fields_and_index_dict(input_ws)
    errors = []

    if expression_column_name not in header_dict:
        click.echo(
            "The entered name is not found in the input: " + expression_column_name)
        sys.exit(1)

    expression_column_letter = header_dict[expression_column_name]

    # use license expression library
    licensing = Licensing()
    expressions = bom_utils.get_expressions(location, expression_column_letter)
    keys = []
    for expression in expressions:
        try:
            keys.extend(licensing.license_keys(expression))
        except:
            msg = "Invalid 'license expression': " + expression
            errors.append(msg)

    unique_license_keys = sorted(set(keys))
    license_data, lic_errors = get_license_data(
        unique_license_keys, api_url, api_key)

    errors.extend(lic_errors)

    if errors:
        # Catch invalid api_url / api_key, display the error and halt
        if len(errors) == 1 and "Invalid 'license" not in errors[0]:
            click.echo(errors[0])
            sys.exit(1)
        quiet = False
        log_file = os.path.join(os.path.dirname(destination), 'error.log')
        utils.report_errors(errors, quiet, log_file)
    license_data.insert(0, ['ScanCode License', 'SPDX Short Identifier',
                        'ScanCode License Category', 'ScanCode License URL'])

    wb = bom_utils.create_nexb_bom(license_data)

    click.echo('Saving License Ref to %s' % destination)
    wb.save(destination)
