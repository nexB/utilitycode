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

from utilitycode import file_cat, file_cat_resource

from commoncode.testcase import FileBasedTesting
import csv
from os.path import dirname, join


file_cat_rules_csv = join(
    dirname(__file__), "../src/utilitycode/file_cat_rules.csv")
rules_list = []

with open(file_cat_rules_csv, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        rules_list.append(row)


class TestFileCat(FileBasedTesting):

    test_data_dir = join(dirname(__file__), 'data')

    def test_validate_matching_in(self):
        value = '.c'
        rule_condition = 'in'
        rules = ['.cpp', '.c', '.java']
        assert file_cat.validate_matching(value, rule_condition, rules)

        value = '.j'
        rule_condition = 'in'
        rules = ['.cpp', '.c', '.java']
        assert not file_cat.validate_matching(value, rule_condition, rules)

    def test_validate_matching_substring(self):
        value = '/prooject/root/share/zoneinfo/test.c'
        rule_condition = 'substring'
        rules = ['/share/zoneinfo/']
        assert file_cat.validate_matching(value, rule_condition, rules)

        value = '/prooject/root/share/t/zoneinfo/test.c'
        rule_condition = 'substring'
        rules = ['/share/zoneinfo/']
        assert not file_cat.validate_matching(value, rule_condition, rules)

    def test_validate_matching_equal(self):
        value = 'test.c'
        rule_condition = 'equal'
        rules = ['test.cpp', 'test.c', 'test.java']
        assert file_cat.validate_matching(value, rule_condition, rules)

        value = 'test.j'
        rule_condition = 'equal'
        rules = ['test.cpp', 'test.c', 'test.java']
        assert not file_cat.validate_matching(value, rule_condition, rules)

    def test_validate_matching_startswith(self):
        value = 'test.c'
        rule_condition = 'startswith'
        rules = ['a', 'test']
        assert file_cat.validate_matching(value, rule_condition, rules)

        value = 'test.c'
        rule_condition = 'startswith'
        rules = ['a', 'atest']
        assert not file_cat.validate_matching(value, rule_condition, rules)

    def test_validate_matching_endswith(self):
        value = 'test.c'
        rule_condition = 'endswith'
        rules = ['.cpp', '.c', '.java']
        assert file_cat.validate_matching(value, rule_condition, rules)

        value = 'test.j'
        rule_condition = 'endswith'
        rules = ['.cpp', '.c', '.java']
        assert not file_cat.validate_matching(value, rule_condition, rules)

    def test_validate_matching_boolean(self):
        value = '.c'
        rule_condition = 'boolean'
        rules = ['True']
        assert file_cat.validate_matching(value, rule_condition, rules)

        value = ''
        rule_condition = 'boolean'
        rules = ['True']
        assert not file_cat.validate_matching(value, rule_condition, rules)

        value = '.c'
        rule_condition = 'boolean'
        rules = ['False']
        assert not file_cat.validate_matching(value, rule_condition, rules)

        value = ''
        rule_condition = 'boolean'
        rules = ['False']
        assert file_cat.validate_matching(value, rule_condition, rules)

    def test_apply_categorize_rules_results_archiveandroid(self):
        value = {
            'path': '',
            'name': '',
            'extension': '.apk',
            'mime_type': '',
            'file_type': '',
            'type': '',
            'programming_language': ''
        }
        resources = [file_cat_resource.Resource.from_dict(value)]
        processed_resources = file_cat.apply_categorize_rules_results(
            resources, rules_list)
        assert processed_resources[0].classname == 'ArchiveAndroid'

    def test_apply_categorize_rules_results_binaryelfo(self):
        value = {
            'path': '',
            'name': '',
            'extension': '.o',
            'mime_type': 'application/x-object',
            'file_type': '',
            'type': '',
            'programming_language': ''
        }
        resources = [file_cat_resource.Resource.from_dict(value)]
        processed_resources = file_cat.apply_categorize_rules_results(
            resources, rules_list)
        assert processed_resources[0].classname == 'BinaryElfO'

    def test_apply_categorize_rules_results_zoneinfo(self):
        value = {
            'path': '/project/share/zoneinfo/a/b.xx',
            'name': 'b.xx',
            'extension': '.xx',
            'mime_type': '',
            'file_type': '',
            'type': 'file',
            'programming_language': ''
        }
        resources = [file_cat_resource.Resource.from_dict(value)]
        processed_resources = file_cat.apply_categorize_rules_results(
            resources, rules_list)
        assert processed_resources[0].classname == 'Zoneinfo'

        value_c = {
            'path': '/project/share/zoneinfo/a/b.c',
            'name': 'b.c',
            'extension': '.c',
            'mime_type': '',
            'file_type': 'C source',
            'type': 'file',
            'programming_language': 'C source'
        }
        resources = [file_cat_resource.Resource.from_dict(value_c)]
        processed_resources = file_cat.apply_categorize_rules_results(
            resources, rules_list)
        assert processed_resources[0].classname == 'SourceC'

        value_dir = {
            'path': '/project/share/zoneinfo/a/',
            'name': 'a',
            'extension': '',
            'mime_type': '',
            'file_type': '',
            'type': 'directory',
            'programming_language': ''
        }
        resources = [file_cat_resource.Resource.from_dict(value_dir)]
        processed_resources = file_cat.apply_categorize_rules_results(
            resources, rules_list)
        assert processed_resources[0].classname == 'Directory'

    def test_apply_categorize_rules_results_startswith(self):
        value = {
            'path': '/project/test.java',
            'name': 'test.java',
            'extension': '',
            'mime_type': '',
            'file_type': 'Java source abc',
            'type': 'file',
            'programming_language': ''
        }
        resources = [file_cat_resource.Resource.from_dict(value)]
        processed_resources = file_cat.apply_categorize_rules_results(
            resources, rules_list)
        assert processed_resources[0].classname == 'SourceJava'

    def test_apply_categorize_rules_results_python(self):
        value_cache = {
            'path': '/project/__pycache__/test.py',
            'name': 'test.py',
            'extension': '.py',
            'mime_type': '',
            'file_type': '',
            'type': 'file',
            'programming_language': ''
        }
        resources = [file_cat_resource.Resource.from_dict(value_cache)]
        processed_resources = file_cat.apply_categorize_rules_results(
            resources, rules_list)
        assert processed_resources[0].classname == 'Pycache'

        value = {
            'path': '/project/test.py',
            'name': 'test.py',
            'extension': '.py',
            'mime_type': '',
            'file_type': '',
            'type': 'file',
            'programming_language': ''
        }
        resources = [file_cat_resource.Resource.from_dict(value)]
        processed_resources = file_cat.apply_categorize_rules_results(
            resources, rules_list)
        assert processed_resources[0].classname == 'SourcePython'
