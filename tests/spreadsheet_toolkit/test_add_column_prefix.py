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
from spreadsheet_toolkit import add_column_prefix


def test_add_column_prefix():
    input = [{'Resource': '/tmp/test.c', 'license_expression': 'mit'},
             {'Resource': '/tmp/test.h', 'license_expression': 'public-domain'}]
    key = 'test_'
    expected = [{'test_Resource': '/tmp/test.c', 'test_license_expression': 'mit'},
                {'test_Resource': '/tmp/test.h', 'test_license_expression': 'public-domain'}]
    row_list = add_column_prefix.add_prefix(key, input)
    assert row_list == expected
