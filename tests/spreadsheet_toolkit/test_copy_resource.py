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

import os
import sys

from spreadsheet_toolkit import copy_resource
from spreadsheet_toolkit.csv_utils import add_unc, read_csv_rows

from testing_utils import get_test_loc

on_windows = 'win32' in sys.platform

def test_get_resource_path():
    test_input = get_test_loc('copy_resource/input.csv')
    rows = read_csv_rows(test_input)
    parent = get_test_loc('copy_resource')
    errors, result = copy_resource.get_resource_path(rows, parent)
    item1 = os.path.normpath(os.path.join(parent, 'samples/sample1.csv'))
    item2 = os.path.normpath(os.path.join(parent, 'samples/sample2.csv'))
    if on_windows:
        item1 = add_unc(item1)
        item2 = add_unc(item2)
    expected = [item1, item2]
    assert result == expected
    assert len(errors) == 0
