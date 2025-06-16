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
from tempfile import NamedTemporaryFile

import json
import os

import openpyxl

from commoncode.testcase import FileBasedTesting

from utilitycode import inv_to_json


def check_result_equals_expected_json(result, expected_loc, regen=False):
    """
    Check equality between a result collection and the data in an expected_loc
    JSON file. Regen the expected file if regen is True.
    """
    if regen:
        expected = result

        expected_dir = os.path.dirname(expected_loc)
        if not os.path.exists(expected_dir):
            os.makedirs(expected_dir)

        with open(expected_loc, 'w') as ex:
            json.dump(expected, ex, indent=2, separators=(',', ': '))
    else:
        with open(expected_loc) as ex:
            expected = json.load(ex)


class TestInvToJson(FileBasedTesting):
    test_data_dir = os.path.join(
        os.path.dirname(__file__), 'data', 'inv_to_json')

    def test_inv_to_json(self):
        test_loc = self.get_test_loc('test.xlsx')
        expected_loc = self.get_test_loc('test.json')
        wb = openpyxl.load_workbook(test_loc, read_only=True)
        result = inv_to_json.get_reportables_by_path(wb, 'INVENTORY')
        check_result_equals_expected_json(result, expected_loc, regen=False)

    def test_inv_to_json_write_reportables_to_json(self):
        test_loc = self.get_test_loc('test.xlsx')
        expected_loc = self.get_test_loc('test_cli-expected.json')
        wb = openpyxl.load_workbook(test_loc, read_only=True)
        reportables = inv_to_json.get_reportables_by_path(wb, 'INVENTORY')
        with NamedTemporaryFile(suffix='.json') as output:
            output_loc = output.name
        inv_to_json.write_reportables_to_json(reportables, output_loc)
        with open(output_loc) as f:
            results = json.load(f)
        check_result_equals_expected_json(results, expected_loc, regen=False)
