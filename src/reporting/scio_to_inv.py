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

from utilitycode import bom_utils
from utilitycode.bom_utils import get_data_from_xlsx
from utilitycode.bom_utils import get_sheetname_from_xlsx
from utilitycode.bom_utils import format_dict_data_for_xlsx_output

packages_working_sheet_headers = [
    'Status',
    'Notes',
    'ToDo',
    'Issue Ref',
    'Product',
    'Codebase',
    'Package URL (purl)',
    'Package Type',
    'License Category',
    'License Expression',
    'Copyright Holders',
    'Vulnerable',
    'Disclosed',
    'Deployed',
    'Analysis Notes',
    'Homepage URL',
    'Download URL',
    'Other URL',
    'Detected License Expression',
    'Detected Copyright Holder',
    'Detected Copyright Notice',
    'Primary Language',
    'Description',
    'Parties',
    'Package Unique ID',
    'sha1',
    'copyright',
    'other_license_expression',
    'notice_text',
    'declared_license_expression_spdx',
    'other_license_expression_spdx',
    'bug_tracking_url',
    'code_view_url',
    'vcs_url',
    'repository_homepage_url',
    'api_data_url',
    'repository_download_url',
    'namespace',
    'name',
    'version',
    'qualifiers',
    'subpath',
    'package_uid',
    'datasource_id',
    'file_references',
    'source_packages',
    'size',
    'md5',
    'sha1',
    'sha256',
    'sha512',
    'release_date',
    'keywords',
    'missing_resources',
    'modified_resources',
    'xlsx_errors'
]

packages_no_reported_fields_headers = [
    'purl',
    'type',
    'declared_license_expression',
    'holder',
    'copyright',
    'homepage_url',
    'download_url',
    'primary_language',
    'parties',
    'package_uid',
    'sha1',
    'size',
    'notice_text',
    'other_license_expression',
    'declared_license_expression_spdx',
    'other_license_expression_spdx',
    'api_data_url',
    'bug_tracking_url',
    'code_view_url',
    'vcs_url',
    'repository_homepage_url',
    'repository_download_url',
    'datasource_id',
    'description',
    'namespace',
    'name',
    'version',
    'qualifiers',
    'subpath',
    'source_packages',
    'file_references',
    'keywords',
    'release_date',
    'missing_resources',
    'modified_resources',
    'md5',
    'sha256',
    'sha512',
    'xlsx_errors'
]

dependencies_target_order = [
    'for_package_uid',
    'package_type',
    'purl',
    'extracted_requirement',
    'scope',
    'is_runtime',
    'is_optional',
    'is_resolved',
    'datasource_id',
    'datafile_path',
    'dependency_uid',
    'xlsx_errors'
]

resources_working_sheet_headers = [
    'analysis_priority',
    'file_category',
    'file_subcategory',
    'Status',
    'Notes',
    'ToDo',
    'Issue Ref',
    'Product',
    'Codebase',
    'Resource Path',
    'Resource Name',
    'Resource Type',
    'for_packages',
    'License Category',
    'License Expression',
    'Copyright Holders',
    'Disclosed',
    'Deployed',
    'Analysis Notes',
    'Homepage URL',
    'Download URL',
    'Other URL',
    'Detected License Expression',
    'Detected Copyright Holders',
    'Detected Copyright Notice',
    'tag',
    'size',
    'sha1',
    'mime_type',
    'file_type',
    'status',
    'extension',
    'emails',
    'urls',
    'authors',
    'detected_license_expression_spdx',
    'percentage_of_license_text',
    'package_data',
    'md5',
    'sha256',
    'sha512',
    'is_binary',
    'is_text',
    'is_archive',
    'is_media',
    'is_key_file',
    'xlsx_errors'
]

resources_no_reported_fields_headers = [
    'path',
    'name',
    'type',
    'for_packages',
    'status',
    'detected_license_expression',
    'holders',
    'copyrights',
    'size',
    'emails',
    'tag',
    'sha1',
    'urls',
    'mime_type',
    'file_type',
    'extension',
    'programming_language',
    'sha512',
    'detected_license_expression_spdx',
    'percentage_of_license_text',
    'authors',
    'package_data',
    'is_binary',
    'is_key_file',
    'is_text',
    'is_archive',
    'is_media',
    'md5',
    'sha256',
    'xlsx_errors'
]


def process_packages_data_field(info_list):
    """
    Return a list of dictionary from the PACKAGES worksheet with the following
    mapping.

    <PACKAGES Field> - <SCIO Field>
    -------------------------------
    Package URL (purl) - purl
    Package Type - type
    License Expression - declared_license_expression
    Copyright Holders - holder
    Homepage URL - homepage_url
    Download URL - download_url
    Detected License Expression - declared_license_expression
    Detected Copyright Holder - holder
    Detected Copyright Notice - copyright
    Primary Language - primary_language
    Description - description
    Parties - parties
    Package Unique ID - package_uid

    For the rest that do not have mapping field will keep the original value
    """
    updated_list = []
    for info_dict in info_list:
        updated_dict = {}
        for key in info_dict:
            if key == 'purl':
                updated_dict['Package URL (purl)'] = info_dict['purl']
            elif key == 'type':
                updated_dict['Package Type'] = info_dict['type']
            elif key == 'declared_license_expression':
                updated_dict['License Expression'] = info_dict['declared_license_expression']
                updated_dict['Detected License Expression'] = info_dict['declared_license_expression']
            elif key == 'holder':
                updated_dict['Copyright Holders'] = info_dict['holder']
                updated_dict['Detected Copyright Holder'] = info_dict['holder']
            elif key == 'homepage_url':
                updated_dict['Homepage URL'] = info_dict['homepage_url']
            elif key == 'download_url':
                updated_dict['Download URL'] = info_dict['download_url']
            elif key == 'copyright':
                updated_dict['Detected Copyright Notice'] = info_dict['copyright']
                updated_dict['copyright'] = info_dict['copyright']
            elif key == 'primary_language':
                updated_dict['Primary Language'] = info_dict['primary_language']
            elif key == 'description':
                updated_dict['Description'] = info_dict['description']
            elif key == 'parties':
                updated_dict['Parties'] = info_dict['parties']
            elif key == 'package_uid':
                updated_dict['Package Unique ID'] = info_dict['package_uid']
            else:
                updated_dict[key] = info_dict[key]
        updated_list.append(updated_dict)
    return updated_list


def add_and_order_fields(field_list, headers_order):
    """
    Return the formatted list with correct fields and orders
    """
    updated_list = []
    for package_content in field_list:
        package_inv_dict = {}
        non_inv_dict = {}
        for header in headers_order:
            if header in package_content:
                package_inv_dict[header] = package_content[header]
            else:
                package_inv_dict[header] = ''
        for k in package_content:
            if not k in package_inv_dict:
                non_inv_dict[k] = package_content[k]
        merged_dict = {**package_inv_dict, **non_inv_dict}
        updated_list.append(merged_dict)
    return updated_list


def process_resources_data_field(info_list):
    """
    Return a list of dictionary from the RESOURCES worksheet with the
    following mapping.

    <RESOURCES Field> - <SCIO Field>
    --------------------------------
    Resource Path - path
    Resource Name - name
    Resource Type - type
    Detected License Expression - detected_license_expression
    Detected Copyright - copyrights
    Detected Copyright Holder - holders

    For the rest that do not have mapping field will keep the original value
    """
    updated_list = []
    for info_dict in info_list:
        updated_dict = {}
        for key in info_dict:
            if key == 'path':
                updated_dict['Resource Path'] = info_dict['path']
            elif key == 'name':
                updated_dict['Resource Name'] = info_dict['name']
            elif key == 'type':
                updated_dict['Resource Type'] = info_dict['type']
            elif key == 'detected_license_expression':
                updated_dict['Detected License Expression'] = info_dict['detected_license_expression']
            elif key == 'copyrights':
                updated_dict['Detected Copyright Notice'] = info_dict['copyrights']
            elif key == 'holders':
                updated_dict['Detected Copyright Holders'] = info_dict['holders']
            else:
                updated_dict[key] = info_dict[key]
        updated_list.append(updated_dict)
    return updated_list


@click.command()
@click.option('--package',
              metavar='name',
              help='Package worksheet name from the INPUT. (Default: PACKAGES)')
@click.option('--resource',
              metavar='name',
              help='Resource worksheet name from the INPUT. (Default: RESOURCES)')
@click.option('--reorder',
              is_flag=True,
              help='Format and reorder all the original columns from the input.\n'
              'See "packages_no_reported_fields_headers" and "resources_no_reported_fields_headers" for the order.')
@click.argument('input', type=click.Path(exists=True, readable=True))
@click.argument('output', type=click.Path(exists=False), required=True)
@click.help_option('-h', '--help')
def cli(package, resource, reorder, input, output):
    """
    This utility converts an SCIO-generated XLSX file to the inventory format
    we want for analysis and reporting.
    The objective is to reduce manual work and human errors.
    """
    if not input.endswith('.xlsx'):
        raise click.UsageError(
            'ERROR: Invalid input file extension: must be .xlsx.')

    # The key of this dictionary is the worksheet name, and the value is
    # the content of the workseeht (list of dictionary)
    input_data_dict = {}

    package_ws = 'PACKAGES'
    resource_ws = 'RESOURCES'
    if package:
        package_ws = package
    if resource:
        resource_ws = resource

    sheetnames = get_sheetname_from_xlsx(input)

    for sheetname in sheetnames:
        if not sheetname == package_ws and not sheetname == resource_ws:
            sheet_context, _sheet_headers = get_data_from_xlsx(
                input, sheetname)
            if reorder and sheetname == 'DEPENDENCIES':
                updated_dep_list = add_and_order_fields(
                    sheet_context, dependencies_target_order)
                input_data_dict['DEPENDENCIES'] = updated_dep_list
            else:
                input_data_dict[sheetname] = sheet_context
        elif sheetname == package_ws:
            packages_context, _packages_headers = get_data_from_xlsx(
                input, package_ws)
            if reorder:
                updated_packages_list = add_and_order_fields(
                    packages_context, packages_no_reported_fields_headers)
            else:
                packages_list = process_packages_data_field(packages_context)
                updated_packages_list = add_and_order_fields(
                    packages_list, packages_working_sheet_headers)
            input_data_dict[package_ws] = updated_packages_list
        else:
            resources_context, _resources_headers = get_data_from_xlsx(
                input, resource_ws)
            if reorder:
                updated_resources_list = add_and_order_fields(
                    resources_context, resources_no_reported_fields_headers)
            else:
                resources_list = process_resources_data_field(
                    resources_context)
                updated_resources_list = add_and_order_fields(
                    resources_list, resources_working_sheet_headers)
            input_data_dict[resource_ws] = updated_resources_list

    formatted_input_data_dict = {}
    for sheetname in input_data_dict:
        formatted_input_data_dict[sheetname] = format_dict_data_for_xlsx_output(
            input_data_dict[sheetname])

    wb = bom_utils.create_scio2inv_bom(
        formatted_input_data_dict, package_ws, resource_ws, reorder)

    click.echo('Saving BOM to %s' % output)
    wb.save(output)
