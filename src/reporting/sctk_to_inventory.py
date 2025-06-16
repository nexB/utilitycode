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
import json

from utilitycode import bom_utils

ignore_scancode_fields = [
    # We always use sha1 for hashes
    'md5',
    'date',
    'sha256',

    # These fields are not used for analysis
    'is_binary',
    'is_text',
    'is_archive',
    'is_media',
    'is_source',
    'is_script',

    # These fields are not used for analysis:
    'files_count',
    'dirs_count',
    'size_count',

    # These fields are derived from license_expression. We will run the lcat
    # utility to fill in License Category and License Name based on Concluded
    # License Expression at the end of analysis phase.
    'license__name',
    'license__short_name',
    'license__category',
    'license__is_exception',
    'license__is_unknown    ',
    'license__owner    ',
    'license__homepage_url',
    'license__text_url',
    'license__reference_url',
    'license__scancode_text_url',
    'license__scancode_data_url',
    'license__spdx_license_key',
    'icense__spdx_url',

    # We rarely use these fields
    'matched_rule__license_expression',
    'matched_rule__licenses',
    'matched_rule__referenced_filenames',
    'matched_rule__is_license_text',
    'matched_rule__is_license_notice',
    'matched_rule__is_license_reference',
    'matched_rule__is_license_tag',
    'matched_rule__is_license_intro',
    'matched_rule__has_unknown',
    'matched_rule__matcher',
    'matched_rule__rule_length',
    'matched_rule__matched_length',
    'matched_rule__match_coverage',
    'matched_rule__rule_relevance',

    # We always use sha1 for hashes:
    'package__md5',
    'package__sha256',
    'package__sha512'
]

fields_header = [
    'analysis_priority',
    'file_category',
    'file_subcategory',
    'Party',
    'Status',
    'Notes',
    'ToDo',
    'Issue Ref#',
    'Product',
    'Module',
    'Codebase',
    'Resource Path',
    'Resource Name',
    'Item Ref',
    'Item Type',
    'Component Name',
    'Component Version',
    'Package Type',
    'Package Namespace',
    'Package Name',
    'Package Version',
    'License Category',
    'License Name',
    'Attribution',
    'Redistribution',
    'Concluded License Expression',
    'Concluded Copyright Holder',
    'Modified',
    'Disclosed',
    'Deployed',
    'Internal Use Only',
    'Details',
    'Analysis Notes',
    'Homepage URL',
    'Download URL',
    'License URL',
    'purl',
    'Detected License Expression',
    'Detected Copyright',
    'Language'
]

package_fields = [
    'package__type',
    'package__namespace',
    'package__name',
    'package__version',
    'package__qualifiers',
    'package__subpath',
    'package__primary_language',
    'package__description',
    'package__release_date',
    'package__parties',
    'package__keywords',
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
    'package__dependencies',
    'package__contains_source_code',
    'package__source_packages',
    'package__extra_data',
    'package__purl',
    'package__repository_homepage_url',
    'package__repository_download_url',
    'package__api_data_url'
]


def get_data_from_json(location):
    """
    Extract data from Scancode's JSON file and return a list of dictionaries
    """
    with open(location) as json_file:
        data = json.load(json_file)
        package_field_list = ['packages', 'package_manifests', 'package_data']
        package_field_name = None
        for entry in data.get('files'):
            if not package_field_name:
                for key in package_field_list:
                    if entry.get(key):
                        package_field_name = key
                        break
            else:
                break
        content_list = data.get('files')
        return content_list, package_field_name


def update_data_field(info_list, package_field_name, report=False):
    """
    Resource Path - from path
    Resource Name - from name

    Item Type - from type

    Detected License Expression - from license_expression OR
    detected_license_expression OR from package__license_expression Detected
    Copyright - from holders OR from package__copyright Language - from
    programming_language OR from package__primary_language
    """
    updated_list = []
    for info_dict in info_list:
        updated_dict = {}
        for key in info_dict:
            if key == 'path':
                if report:
                    updated_dict['Resource Path'] = info_dict['path']
                updated_dict['path'] = info_dict['path']
            elif key == 'name':
                if report:
                    updated_dict['Resource Name'] = info_dict['name']
                updated_dict['name'] = info_dict['name']
            elif key == 'programming_language':
                if report:
                    updated_dict['Language'] = info_dict['programming_language']
                updated_dict['programming_language'] = info_dict['programming_language']
            elif key == 'type':
                if info_dict['type'] == 'file':
                    if report:
                        updated_dict['Item Type'] = 'F'
                elif info_dict['type'] == 'directory':
                    if report:
                        updated_dict['Item Type'] = 'D'
                updated_dict['type'] = info_dict['type']
            elif key == 'licenses':
                lic_key, lic_score = construct_licenses_data(info_dict[key])
                updated_dict['license_key'] = lic_key
                updated_dict['license_score'] = lic_score
            elif key == package_field_name:
                updated_dict[package_field_name] = update_packages_list(
                    info_dict[key])
                # Put the package_primary language for Language if no value for
                # programming language
                if updated_dict[package_field_name]:
                    if report:
                        if not updated_dict['Language']:
                            # Get the first "primary_language" value from the
                            # "packages" list
                            updated_dict['Language'] = updated_dict[package_field_name][0]['primary_language']
                    # We want to integrate the package data into the main
                    # row if there is only one package data
                    if len(updated_dict[package_field_name]) == 1:
                        new_dict = integrate_package_data(
                            updated_dict[package_field_name])
                        for key in new_dict:
                            updated_dict[key] = data_str_convertion(
                                new_dict[key])
            elif isinstance(info_dict[key], dict):
                value = ""
                # Convert the dictionary into string
                if info_dict[key]:
                    value_list = []
                    for item in info_dict[key]:
                        content = item + ': ' + str(info_dict[key][item])
                        value_list.append(content)
                    value = '\n'.join(value_list)
                updated_dict[key] = value
            elif isinstance(info_dict[key], list):
                value = ""
                if info_dict[key]:
                    # For list element which is str such as
                    # "license_expressions"
                    if isinstance(info_dict[key][0], dict):
                        # For list element which is a dictionary such as
                        # "copyrights" etc. Most of the key for the useful
                        # information from dictionary is "value" with an
                        # exception that "url" is used in "urls" dictionary and
                        # "emai" is used in "emails" Updated: The format output
                        # is updated as it no longer uses the 'value' as the
                        # key, but I will still keep the "old" code to get the
                        # 'value' for backward compatibility. Deduplication
                        # will be performed
                        value_list = []
                        for item in info_dict[key]:
                            if 'value' in item:
                                if item['value'] not in value_list:
                                    value_list.append(item['value'])
                            elif 'copyright' in item:
                                if item['copyright'] not in value_list:
                                    value_list.append(item['copyright'])
                            elif 'holder' in item:
                                if item['holder'] not in value_list:
                                    value_list.append(item['holder'])
                            elif 'author' in item:
                                if item['author'] not in value_list:
                                    value_list.append(item['author'])
                            elif 'url' in item:
                                if item['url'] not in value_list:
                                    value_list.append(item['url'])
                            elif 'email' in item:
                                if item['email'] not in value_list:
                                    value_list.append(item['email'])
                        value = '\n'.join(value_list)
                    else:
                        value = '\n'.join(info_dict[key])
                updated_dict[key] = value
                if value and key == 'license_expressions' and report:
                    updated_dict['Detected License Expression'] = value
                elif value and key == 'detected_license_expression' and report:
                    updated_dict['Detected License Expression'] = value
                elif key == 'holders' and report:
                    updated_dict['Detected Copyright'] = value
            else:
                updated_dict[key] = info_dict[key]
        updated_list.append(updated_dict)

    return updated_list


def integrate_package_data(package_list):
    """
    Insert the 'package__' prefix to the dictionary keys
    """
    dict = {}
    # There is only one dictionary in the package list
    for key in package_list[0]:
        new_key = 'package__' + key
        dict[new_key] = package_list[0][key]
    return dict


def construct_licenses_data(lic_list):
    """
    Extract only the key and score from the "licenses" field
    """
    lic_key = ''
    lic_score = ''
    for lic_dict in lic_list:
        lic_key += str(lic_dict['key']) + '\n'
        lic_score += str(lic_dict['score']) + '\n'
    return lic_key.strip(), lic_score.strip()


def update_packages_list(packages):
    """
    Update the packages list. Convert all the purl of the package dependencies
    to string instead of a list of dictionary
    """
    updated_package_list = []
    for package in packages:
        updated_package_dict = {}
        for key in package:
            if key == "dependencies":
                purls = ""
                for dep in package['dependencies']:
                    if dep['purl']:
                        purls += dep['purl'] + '\n'
                updated_package_dict['dependencies'] = purls.strip()
            else:
                updated_package_dict[key] = package[key]
        updated_package_list.append(updated_package_dict)
    return updated_package_list


def construct_package_rows(package_dict, output_fields, package_field_name):
    """
    Construct new row which only contain the package information and the
    Resource Path

    Homepage URL - from package__homepage_url if present Download URL - from
    package__download_url if present Item Ref - from package__purl if present
    purl - from package__purl if present Package Type - from package__type
    Package Namespace - from package__namespace Package Name - from
    package__name Package Version - from package__version
    """
    packages_rows = []
    for package in package_dict[package_field_name]:
        row = []
        for header in output_fields:
            if header == 'Resource Path':
                row.append(package_dict[header])
            elif header == 'Homepage URL' and package['homepage_url']:
                row.append(package['homepage_url'])
            elif header == 'Download URL' and package['download_url']:
                row.append(package['download_url'])
            elif header == 'Item Ref' and package['purl']:
                row.append(package['purl'])
            elif header == 'purl' and package['purl']:
                row.append(package['purl'])
            elif header == 'Package Type' and package['type']:
                row.append(package['type'])
            elif header == 'Package Namespace' and package['namespace']:
                row.append(package['namespace'])
            elif header == 'Package Name' and package['name']:
                row.append(package['name'])
            elif header == 'Package Version' and package['version']:
                row.append(package['version'])
            elif header.startswith('package__'):
                for p_field in package_fields:
                    if header == p_field:
                        key = p_field.replace('package__', '')
                        if key in package:
                            if package[key]:
                                value = data_str_convertion(package[key])
                                row.append(value)
                            else:
                                row.append("")
                        break
            else:
                row.append("")
        packages_rows.append(row)
    return packages_rows


def data_str_convertion(data):
    """
    list and dictionary formatted data cannot be written in Excel
    We need special treatment (i.e. convert it to string) for these
    """
    value = ''
    if data:
        if isinstance(data, list):
            try:
                value = '\n'.join(data)
            except:
                value += data_str_convertion(data[0])
        elif isinstance(data, dict):
            for k in data:
                if data[k]:
                    try:
                        value += k + ": " + data[k] + '\n'
                    except:
                        value += k + ": " + data_str_convertion(data[k])
        else:
            value = str(data)
    return value.strip()


def remove_ignore_scancode_fields(list):
    """
    Return a new list with all the ignore_scancode_fields removed from the list
    """
    updated_list = []
    for header in list:
        if header not in ignore_scancode_fields:
            updated_list.append(header)
    return updated_list


def construct_data(info_dict, package_field_name, report):
    """
    Construct the list of needed data from the input and return it
    Special treatment for "packages" as we don't want to "flatten" these values
    """
    data = []
    output_fields = []
    if report:
        updated_fields_header = remove_ignore_scancode_fields(fields_header)
        updated_package_fields = remove_ignore_scancode_fields(package_fields)
        output_fields = updated_fields_header
        for dict in info_dict:
            for key in dict:
                if key not in output_fields and key not in ignore_scancode_fields and not key.startswith('package__'):
                    # Will handle the package_fields later
                    if not key == package_field_name:
                        output_fields.append(key)

        for package_field in updated_package_fields:
            output_fields.append(package_field)
    else:
        for dict in info_dict:
            for key in dict:
                if key not in output_fields:
                    output_fields.append(key)

    for dict in info_dict:
        row = []
        for header in output_fields:
            if header in dict.keys():
                row.append(dict[header])
            else:
                # We will integrate the package information into the main row if
                # there is only one package.
                if package_field_name and len(dict[package_field_name]) == 1:
                    value = ''
                    if header == 'Homepage URL':
                        value = dict[package_field_name][0]['homepage_url']
                    elif header == 'Download URL':
                        value = dict[package_field_name][0]['download_url']
                    elif header == 'Item Ref':
                        value = dict[package_field_name][0]['purl']
                    elif header == 'purl':
                        value = dict[package_field_name][0]['purl']
                    elif header == 'Package Type':
                        value = dict[package_field_name][0]['type']
                    elif header == 'Package Namespace':
                        value = dict[package_field_name][0]['namespace']
                    elif header == 'Package Name':
                        value = dict[package_field_name][0]['name']
                    elif header == 'Package Version':
                        value = dict[package_field_name][0]['version']
                    if value:
                        row.append(value)
                    else:
                        row.append("")
                else:
                    row.append("")
        data.append(row)
        # We don't want to flatten any package information and therefore we
        # are writing new rows if it has more than one package information
        if package_field_name and dict[package_field_name] and len(dict[package_field_name]) > 1:
            for row in construct_package_rows(dict, output_fields, package_field_name):
                data.append(row)

    output_data = []
    output_data.append(output_fields)
    for info in data:
        output_data.append(info)
    return output_data


@click.command()
@click.option('--report',
              is_flag=True,
              help='Generate an project INVENTORY worksheet.')
@click.argument('location', type=click.Path(exists=True, readable=True))
@click.argument('destination', type=click.Path(exists=False), required=True)
@click.help_option('-h', '--help')
def cli(report, location, destination):
    """
    This utility will convert a ScanCode Toolkit scan file to a XLSX file.
    The objective is to reduce manual work and errors by automating a
    manual task.
    """
    if not location.endswith('.json'):
        raise click.UsageError('ERROR: "The input is not a .json file.')

    info_list, concluded_package_field_name = get_data_from_json(location)
    updated_info_list = update_data_field(
        info_list, concluded_package_field_name, report)

    data = construct_data(
        updated_info_list, concluded_package_field_name, report)

    wb = bom_utils.create_nexb_bom_from_scancode(data, report)
    click.echo('Saving BOM to %s' % destination)
    wb.save(destination)
