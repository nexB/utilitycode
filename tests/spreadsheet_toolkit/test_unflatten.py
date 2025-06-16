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
from spreadsheet_toolkit import unflatten


def test_unflattening():
    input = [{'Resource': '/tmp/test.c', 'name': 'test.c', 'license_expression': 'mit\napache-2.0', 'type': 'file'},
             {'Resource': '/tmp/test.h', 'name': '', 'license_expression': 'public-domain', 'type': 'file'}]
    expected = [{'Resource': '/tmp/test.c', 'name': 'test.c', 'license_expression': 'mit', 'type': 'file'},
                {'Resource': '/tmp/test.c', 'name': 'test.c',
                    'license_expression': 'apache-2.0', 'type': 'file'},
                {'Resource': '/tmp/test.h', 'name': '', 'license_expression': 'public-domain', 'type': 'file'}]
    headers = ['Resource', 'name', 'license_expression', 'type']
    key = 'license_expression'
    result = unflatten.unflattening(headers, input, key)
    assert result == expected
