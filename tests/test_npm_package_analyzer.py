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

import json
import os

from commoncode.testcase import FileBasedTesting
from utilitycode import npm_package_analyzer


class TestPackageLockParse(FileBasedTesting):

    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_update_package_with_data(self):
        test_package = npm_package_analyzer.Package('debug', '3.1.0')
        test_data_file = self.get_test_loc('lock_files/debug-3.1.0.json')
        with open(test_data_file) as f:
            test_data = json.load(f)

        npm_package_analyzer.update_package_with_data(test_package, test_data)

        assert test_package.tk_package.name == 'debug'
        assert test_package.tk_package.version == '3.1.0'
        assert test_package.tk_package.declared_license_expression == 'mit'

    def test_LockPackage_api_url(self):
        test_name = 'node'
        test_version = '0.0.0'

        result = npm_package_analyzer.Package(
            test_name, test_version).api_url()

        assert result == 'https://registry.npmjs.org/node/'

    def test_create_packages(self):
        test_deps = [('browser-stdout', '1.3.1'), ('commander', '2.15.1')]
        result = list(npm_package_analyzer.create_packages(test_deps))

        assert result[0].name == 'browser-stdout'
        assert result[0].version == '1.3.1'

        assert result[1].name == 'commander'
        assert result[1].version == '2.15.1'

    def test_get_name_version_from_json(self):
        test_data_file = self.get_test_loc('lock_files/package_scancode.json')
        expected = [('agent-base', '4.2.1'), ('es6-promise', '4.2.5')]
        output, err = npm_package_analyzer.get_name_version_from_json(
            test_data_file)
        assert output == expected

    def test_get_name_version_from_purl(self):
        purl1 = 'pkg:npm/agent-base@4.2.1'
        purl2 = 'pkg:npm/es6-promise@4.2.5'
        expected_name1 = 'agent-base'
        expected_version1 = '4.2.1'
        expected_name2 = 'es6-promise'
        expected_version2 = '4.2.5'
        result_name1, result_version1 = npm_package_analyzer.get_name_version_from_purl(
            purl1)
        result_name2, result_version2 = npm_package_analyzer.get_name_version_from_purl(
            purl2)
        assert result_name1 == expected_name1
        assert result_version1 == expected_version1
        assert result_name2 == expected_name2
        assert result_version2 == expected_version2
