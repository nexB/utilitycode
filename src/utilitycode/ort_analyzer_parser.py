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
import yaml

from utilitycode.bom_utils import create_multiple_worksheets_xlsx_output
from utilitycode.bom_utils import format_dict_data_for_xlsx_output

data_list = []
format_repo_list = []


def get_repository_data(result_dict, parent_name=None):
    """
    Return a list of formatted dictionary that contains the repository information
    Example:
        {'vcs': {'type': 'Git', 'url': 'git@github.com:test/framework.git', 'revision': '123', 'path': 'app/test'},
        'vcs_processed': {'type': 'Git', 'url': 'ssh://git@github.com/test/framework.git', 'revision': '456', 'path': 'app/test1'}, 'config': {}}

    Return:
        {'vcs_type': 'Git', 'vcs_url': 'git@github.com:test/framework.git', 'vcs_revision': '123', 'vcs_path': 'app/test',
        'vcs_processed_type': 'Git', 'vcs_processed_url': 'ssh://git@github.com/test/framework.git', 'vcs_processed_revision': '456', 'vcs_processed_path': 'app/test1'}
    """
    for key in result_dict:
        output_dict = recursive_dict_handler(
            result_dict[key], key)
        if output_dict:
            data_list.append(output_dict)
    return data_list


def recursive_dict_handler(data_dict, parent_name=None):
    """
    Return the desire key and value where the value is not a dictionay
    """
    output_dict = {}
    for k in data_dict:
        if parent_name:
            key_name = parent_name + '_' + k
        else:
            key_name = k

        if isinstance(data_dict[k], dict):
            output_dict = recursive_dict_handler(
                data_dict[k], key_name)
        elif isinstance(data_dict[k], list):
            for item in data_dict[k]:
                if not isinstance(item, dict):
                    output_dict[key_name] = '\n'.join(data_dict[k])
                else:
                    output_dict = recursive_dict_handler(
                        item, key_name)
                    data_list.append(output_dict)
                    output_dict = {}
        else:
            output_dict[key_name] = data_dict[k]
    return output_dict


def get_result_data(result_list):
    """
    Return a list of extracted packages data
    """
    data_list = []
    for data_dict in result_list:
        data_list.append(extract_result_data(data_dict))
    return data_list


def extract_result_data(result_dict, parent_name=None):
    """
    Given a dictionary, return a list of formatted dictionary
    that contains the data information
    Example:
        [{'id': 'NPM::JSONStream:1.3.5', 'purl': 'pkg:npm/JSONStream@1.3.5',
        'authors': ['Dominic Tarr', 'Foo'], 'declared_licenses_processed':
        {'spdx_expression': 'Apache-2.0 OR MIT'}, 'binary_artifact': {'url': '',
        'hash': {'value': '', 'algorithm': ''}}}]

    Return:
        [{'id': 'NPM::JSONStream:1.3.5', 'purl': 'pkg:npm/JSONStream@1.3.5',
        'authors': 'Dominic Tarr\n Foo,
        declared_licenses_processed_spdx_expression': 'Apache-2.0 OR MIT',
        'binary_artifact_url': '', 'binary_artifact_hash_value': '',
        'binary_artifact_hash_algorithm': ''}]
    """
    data_dict = {}
    for key in result_dict:
        if isinstance(result_dict[key], list):
            data_dict[key] = '\n'.join(result_dict[key])
        elif isinstance(result_dict[key], dict):
            if parent_name:
                parent_key_name = parent_name + '_' + key
            else:
                parent_key_name = key
            nested_dict = extract_result_data(
                result_dict[key], parent_key_name)
            data_dict.update(nested_dict)
        else:
            if parent_name:
                key_name = parent_name + '_' + key
            else:
                key_name = key
            data_dict[key_name] = result_dict[key]
    return data_dict


def process_dg_data_and_format_for_output(dep_graph_dict):
    formatted_list_for_xlsx_output = []
    dg_packages_dict = {}
    dep_graph_package_list = []
    dep_graph_scope_dict = {}
    for package_manager in dep_graph_dict:
        dep_graph_package_list = dep_graph_dict[package_manager]['packages']
        dep_graph_scope_dict = dep_graph_dict[package_manager]['scopes']
        break
    # Create a dictionary which have the index as the key and package name
    # as the value
    for index, package_name in enumerate(dep_graph_package_list):
        dg_packages_dict[index] = package_name

    # Get all the possible "header"
    headers = []
    for project in dep_graph_scope_dict:
        # dep_graph_scope_dict[project] is a list of dictionary value such as
        # [{'root': 0}, {'root': 1, 'fragment': 2}]
        for scope in dep_graph_scope_dict[project]:
            for key in scope:
                if key not in headers:
                    headers.append(key)
    output_headers = ['Project'] + headers
    formatted_list_for_xlsx_output.append(output_headers)
    for project in dep_graph_scope_dict:
        for scope in dep_graph_scope_dict[project]:
            row_entry_list = [project]
            for header in headers:
                if header in scope:
                    row_entry_list.append(dg_packages_dict[scope[header]])
                else:
                    row_entry_list.append('')
            formatted_list_for_xlsx_output.append(row_entry_list)
    return formatted_list_for_xlsx_output


def process_dg_data(package_manager, dep_graph_package_list, dep_graph_scope_dict, packages_data_list):
    dg_packages_dict = {}
    dg_output_list = []
    # Create a dictionary which have the index as the key and package name
    # as the value
    for index, package_name in enumerate(dep_graph_package_list):
        dg_packages_dict[index] = package_name

    for project in dep_graph_scope_dict:
        project_name = project.rpartition(':')[0]
        scope_name = project.rpartition(':')[2]
        for scope in dep_graph_scope_dict[project]:
            row_entry_dict = {'package_manager': package_manager}
            row_entry_dict['project'] = project_name
            row_entry_dict['scope_name'] = scope_name
            package_id = dg_packages_dict[scope['root']]
            row_entry_dict['id'] = package_id
            for package in packages_data_list:
                if package['id'] == package_id:
                    row_entry_dict['purl'] = package['purl']
                    break
            copy_dict = copy.deepcopy(row_entry_dict)
            dg_output_list.append(copy_dict)
            row_entry_dict.clear()
    return dg_output_list


def map_package_name(dep_graph_nodes_list, packages_data_list):
    """
    Return a list of dictionaries of the mapped index to the package name
    """
    mapped_list = []
    for node in dep_graph_nodes_list:
        # fragment is not useful for the context, only the "pkg" will be
        # used and mapped
        pkg_dict = {}
        if 'pkg' in node:
            pkg_dict['pkg'] = packages_data_list[node['pkg']]
        mapped_list.append(pkg_dict)
    return mapped_list


def process_package_dep(package_manager, dep_graph_nodes_package_name_list, dep_graph_edges_list, packages_data_list):
    packages_dict = {}
    output_list = []
    # Create a dictionary which have the index as the key and package name
    # as the value
    for index, package_name in enumerate(dep_graph_nodes_package_name_list):
        if "pkg" in package_name:
            packages_dict[index] = package_name['pkg']
        else:
            packages_dict[index] = ""

    for edge in dep_graph_edges_list:
        edge_dict = {}
        edge_dict = {'package_manager': package_manager}

        package_name = packages_dict[edge['from']]
        pacakge_dep_name = packages_dict[edge['to']]

        edge_dict['packages'] = package_name
        edge_dict['purl'] = ""
        edge_dict['dependencies'] = pacakge_dep_name
        edge_dict['dependencies purl'] = ""
        edge_dict['internal use - nodes_index_from'] = edge['from']
        edge_dict['internal use - nodes_index_to'] = edge['to']
        for package in packages_data_list:
            if package['id'] == package_name:
                edge_dict['purl'] = package['purl']
            if package['id'] == pacakge_dep_name:
                edge_dict['dependencies purl'] = package['purl']
        output_list.append(edge_dict)
    return output_list


def format_repo_output_list(repo_list):
    """
    The purpose is to put unique entry field in one row. Put it to another
    row(s) if there is more than one. The input is a list of dictionaries
    For instance,
    [{'name': 'a', 'license': 'mit'}, {'license': 'bsd', 'notice': 'NOTICE'}]
    should become
    [{'name': 'a', 'license': 'mit', 'notice': 'NOTICE'}, {'license': 'bsd'}]
    """
    updated_dict = {}
    left_todo_list = []
    for repo in repo_list:
        for key in repo:
            if key not in updated_dict:
                updated_dict[key] = repo[key]
            else:
                left_todo_list.append({key: repo[key]})
    copy_dict = copy.deepcopy(updated_dict)
    format_repo_list.append(copy_dict)

    if left_todo_list:
        format_repo_output_list(left_todo_list)


def package_id_to_purl(package_id, packages_data_list):
    for package in packages_data_list:
        if package['id'] == package_id:
            return package['purl']
    return ""


def process_dg_data_flatten(dep_graph_dict, packages_data_list):
    output_list = []
    for package_manager in dep_graph_dict:
        if 'packages' not in dep_graph_dict[package_manager]:
            continue
        dep_graph_package_list = dep_graph_dict[package_manager]['packages']
        dep_graph_scope_dict = dep_graph_dict[package_manager]['scopes']
        dep_graph_nodes_list = dep_graph_dict[package_manager]['nodes']
        dep_graph_nodes_package_name_list = map_package_name(
            dep_graph_nodes_list, dep_graph_package_list)
        dep_graph_edges_list = dep_graph_dict[package_manager]['edges']

        dg_packages_dict = {}
        # Create a dictionary which have the index as the key and package
        # name as the value
        for index, package_name in enumerate(dep_graph_package_list):
            dg_packages_dict[index] = package_name

        packages_dict = {}
        # Create a dictionary which have the index as the key and package
        # name as the value
        for index, package_name in enumerate(dep_graph_nodes_package_name_list):
            if "pkg" in package_name:
                packages_dict[index] = package_name['pkg']
            else:
                packages_dict[index] = ""

        edge_dict = {}
        for edge in dep_graph_edges_list:

            package_name = packages_dict[edge['from']]
            pacakge_dep_name = packages_dict[edge['to']]

            if package_name not in edge_dict:
                edge_dict[package_name] = [pacakge_dep_name]
            else:
                edge_dict[package_name].append(pacakge_dep_name)

        for project in dep_graph_scope_dict:
            project_name = project.rpartition(':')[0]
            scope_name = project.rpartition(':')[2]
            for scope in dep_graph_scope_dict[project]:
                row_entry_dict = {'package_manager': package_manager}
                row_entry_dict['project'] = project_name
                row_entry_dict['scope_name'] = scope_name
                package_id = dg_packages_dict[scope['root']]
                row_entry_dict['id'] = package_id
                row_entry_dict['purl'] = package_id_to_purl(
                    package_id, packages_data_list)

                if package_id in edge_dict:
                    packages = edge_dict[package_id]
                    row_entry_dict['direct dependencies'] = '\n'.join(packages)
                    direct_dep_purl_list = []
                    indirect_dep_list = []
                    indirect_dep_purl_list = []
                    for package in packages:
                        direct_dep_purl_list.append(
                            package_id_to_purl(package, packages_data_list))
                        if package in edge_dict:
                            # Avoid duplicated packages
                            for dep_package in edge_dict[package]:
                                if dep_package not in indirect_dep_list:
                                    indirect_dep_list.append(dep_package)
                                    indirect_dep_purl_list.append(
                                        package_id_to_purl(dep_package, packages_data_list))

                    if direct_dep_purl_list:
                        row_entry_dict['direct dependencies purl'] = '\n'.join(
                            direct_dep_purl_list)

                    if indirect_dep_list:
                        row_entry_dict['indirect dependencies'] = '\n'.join(
                            indirect_dep_list)
                        row_entry_dict['indirect dependencies purl'] = '\n'.join(
                            indirect_dep_purl_list)
                    else:
                        row_entry_dict['indirect dependencies'] = ""
                else:
                    row_entry_dict['direct dependencies'] = ""
                    row_entry_dict['indirect dependencies'] = ""
                copy_dict = copy.deepcopy(row_entry_dict)
                output_list.append(copy_dict)
                row_entry_dict.clear()

    return output_list


@click.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True))
@click.argument('output', type=click.Path(exists=False), required=True)
@click.help_option('-h', '--help')
def cli(input_file, output):
    """
    Parser and format the ORT's analyzer-result.yml to XLSX
    """
    assert input_file

    if not output.endswith('.xlsx'):
        raise click.UsageError(
            'ERROR: "The output does not ends with \'.xlsx\' extension.')

    # Load the YAML file
    with open(input_file, "r", encoding="utf-8") as yaml_file:
        data = yaml.load(yaml_file, Loader=yaml.FullLoader)
    repo_dict = data['repository']

    analyzer_result_dict = data['analyzer']['result']
    projects_dict = analyzer_result_dict['projects']
    packages_dict = analyzer_result_dict['packages']
    dep_graph_dict = analyzer_result_dict['dependency_graphs']

    repository_data_list = get_repository_data(repo_dict)
    format_repo_output_list(repository_data_list)

    project_data_list = get_result_data(projects_dict)
    packages_data_list = get_result_data(packages_dict)

    dep_graph_flatten_list = []
    dep_graph_flatten_list = process_dg_data_flatten(
        dep_graph_dict, packages_data_list)
    dep_graph_list = []
    dep_graph_packages_dep_list = []
    for package_manager in dep_graph_dict:
        if 'packages' in dep_graph_dict[package_manager]:
            dep_graph_package_list = dep_graph_dict[package_manager]['packages']
            dep_graph_scope_dict = dep_graph_dict[package_manager]['scopes']
            dep_graph_list.extend(process_dg_data(package_manager,
                                                  dep_graph_package_list, dep_graph_scope_dict, packages_data_list))

            dep_graph_nodes_list = dep_graph_dict[package_manager]['nodes']
            dep_graph_nodes_package_name_list = map_package_name(
                dep_graph_nodes_list, dep_graph_package_list)
            dep_graph_edges_list = dep_graph_dict[package_manager]['edges']
            dep_graph_packages_dep_list.extend(process_package_dep(
                package_manager, dep_graph_nodes_package_name_list, dep_graph_edges_list, packages_data_list))

    formatted_repo_data = format_dict_data_for_xlsx_output(
        format_repo_list)
    formatted_project_data = format_dict_data_for_xlsx_output(
        project_data_list)
    formatted_packages_data = format_dict_data_for_xlsx_output(
        packages_data_list)
    formatted_dg_data = format_dict_data_for_xlsx_output(
        dep_graph_list)
    formatted_pacakged_dep = format_dict_data_for_xlsx_output(
        dep_graph_packages_dep_list)
    formatted_dep_graph_flatten = format_dict_data_for_xlsx_output(
        dep_graph_flatten_list)

    data_list = []
    ws_name_list = ['repository_data', 'project',
                    'packages', 'dependency_graphs', 'packages_dependencies',
                    'dependency_graphs_flatten']
    data_list.append(formatted_repo_data)
    data_list.append(formatted_project_data)
    data_list.append(formatted_packages_data)
    data_list.append(formatted_dg_data)
    data_list.append(formatted_pacakged_dep)
    data_list.append(formatted_dep_graph_flatten)

    create_multiple_worksheets_xlsx_output(output, ws_name_list, data_list)

    print("\nFinished!")
