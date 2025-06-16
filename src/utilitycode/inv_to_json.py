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

from __future__ import print_function
from __future__ import absolute_import


import click
import openpyxl
import jsonstreams


@click.command()
@click.argument('input_xlsx', type=click.Path(exists=True, readable=True))
@click.argument('output_location', type=click.Path(exists=False))
@click.help_option('-h', '--help')
def cli(input_xlsx, output_location=None):
    """
    Convert an input XLSX (worksheet named "INVENTORY" and/or
    "INV-DETAILS") to a JSON output. The output will contains the component
    and package information such as name, path, version, license_expression
    etc.
    """
    wb = openpyxl.load_workbook(input_xlsx, read_only=True)
    inv_reportables_by_path = get_reportables_by_path(wb, 'INVENTORY')
    inv_details_reportables_by_path = get_reportables_by_path(
        wb, 'INV-DETAILS')
    combined_reportables_by_path = inv_reportables_by_path.copy()
    combined_reportables_by_path.update(inv_details_reportables_by_path)
    write_reportables_to_json(combined_reportables_by_path, output_location)


def get_reportables_by_path(workbook, sheet_name):
    try:
        inventory_sheet = workbook[sheet_name]
    except KeyError:
        return dict()
    inventory_column_indices = {cell.value.lower(): i for i, cell in enumerate(
        inventory_sheet[1]) if cell.value}
    reportable_by_paths = dict()
    for row in inventory_sheet.iter_rows(min_row=2):
        path = row[inventory_column_indices['item path']].value
        name = row[inventory_column_indices['item name']].value

        license_expressions = []
        license_expression = row[inventory_column_indices['concluded license expression']].value
        if license_expression:
            license_expressions = [license_expression]

        holders = []
        copyright_holders = row[inventory_column_indices['concluded copyright holder']].value
        if copyright_holders:
            holders = [
                {'value': copyright_holders}
            ]

        homepage_url = row[inventory_column_indices['homepage url']].value
        download_url = row[inventory_column_indices['download url']].value

        packages = []
        package_type = row[inventory_column_indices['package type']].value
        package_namespace = row[inventory_column_indices['package namespace']].value
        package_name = row[inventory_column_indices['package name']].value
        package_version = row[inventory_column_indices['package version']].value
        if package_type:
            package_data = dict()
            package_data['type'] = package_type
            package_data['namespace'] = package_namespace
            package_data['name'] = package_name
            package_data['version'] = package_version
            package_data['homepage_url'] = homepage_url
            package_data['download_url'] = download_url
            package_data['copyright'] = copyright_holders
            package_data['license_expression'] = license_expression
            packages = [package_data]

        # TODO: figure out how to handle this
        # TODO: originally added to the extra_data field, but it makes more
        # sense to have it as its own top-level field
        components = []
        component_name = row[inventory_column_indices['component name']].value
        component_version = row[inventory_column_indices['component version']].value
        if component_name:
            component = dict()
            component['name'] = component_name
            component['version'] = component_version
            component['copyright'] = copyright_holders
            component['license_expression'] = license_expression
            component['homepage_url'] = homepage_url
            component['download_url'] = download_url
            components = [component]

        if path not in reportable_by_paths:
            reportable = dict()
            reportable['path'] = path
            reportable['name'] = name
            reportable['license_expressions'] = license_expressions
            reportable['holders'] = holders
            reportable['packages'] = packages
            reportable['components'] = components
            reportable_by_paths[path] = reportable
        else:
            # If we have the same path again, then we are reporting another Package or Component for the same path.
            reportable = reportable_by_paths[path]
            if license_expressions:
                reportable['license_expressions'].extend(license_expressions)
            if holders:
                reportable['holders'].extend(holders)
            if packages:
                reportable['packages'].extend(packages)
            if components:
                reportable['components'].extend(components)
    return reportable_by_paths


def write_reportables_to_json(reportables, json_loc):
    files = [v for _, v in reportables.items()]
    with open(json_loc, 'w') as f:
        with jsonstreams.Stream(
            jsonstreams.Type.OBJECT,
            fd=f,
            indent=2,
            pretty=True
        ) as s:
            s.write('files', files)
