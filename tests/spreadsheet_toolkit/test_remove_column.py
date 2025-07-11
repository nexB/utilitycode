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
from spreadsheet_toolkit import remove_column


def test_remove_header():
    input = ['Resource', 'type', 'name']
    remove_col = ['type']
    result = remove_column.remove_header(input, remove_col)
    expected = ['Resource', 'name']
    assert result == expected


def test_remove_multi_header():
    input = ['Resource', 'type', 'name']
    remove_col = ['type', 'Resource']
    result = remove_column.remove_header(input, remove_col)
    expected = ['name']
    assert result == expected
