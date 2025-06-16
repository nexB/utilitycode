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
from spreadsheet_toolkit import concat

from testing_utils import get_test_loc


def test_concat_csv():
    expected = [{'Resource': '/tmp/', 'name': 'tmp'},
                {'Resource': '/tmp/test.c', 'license_expression': 'mit'}]
    test_input = (get_test_loc('concat/sample1.csv'), get_test_loc('concat/sample2.csv'))
    result = concat.concat_inputs(test_input, None)
    assert result == expected


def test_sync_rows_dict():
    test_input = (get_test_loc('concat/sample1.csv'), get_test_loc('concat/sample2.csv'))
    test_list = concat.concat_inputs(test_input, None)
    result = concat.sync_rows_dict(test_list)
    expected = [{'Resource': '/tmp/', 'name': 'tmp', 'license_expression': ''},
                {'Resource': '/tmp/test.c', 'name': '', 'license_expression': 'mit'}]
    assert result == expected
