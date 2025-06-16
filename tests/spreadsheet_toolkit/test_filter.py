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
from spreadsheet_toolkit import filter


def test_get_filtering_keys_values():
    exp1 = (u'license_expression',)
    exp2 = (u'license_expression=mit',)
    expect1 = [{u'license_expression': True}]
    expect2 = [{u'license_expression': [u'mit']}]
    result1 = filter.get_filtering_keys_values(exp1)
    assert result1 == expect1
    result2 = filter.get_filtering_keys_values(exp2)
    assert result2 == expect2


def test_simple_include_filtering():
    input = {'notes': 'a', 'Resource': '/project/123/sample1.c'}
    include_condition1 = [{u'notes': [u'a']}]
    result1 = filter.include_filtering(input, include_condition1)
    assert result1 == input
    include_condition2 = [{u'notes': [u'b']}]
    result2 = filter.include_filtering(input, include_condition2)
    assert result2 == None


def test_or_include_filtering():
    include_condition = [{u'notes': [u'a', u'b'], u'Resource': [u'.java']}]
    input = {'notes': 'b', 'Resource': '/project/123/'}
    result = filter.include_filtering(input, include_condition)
    assert result == input


def test_include_filtering_with_true_condition():
    include_condition = [{u'license_expression': True}]
    input1 = {'license_expression': 'mit'}
    input2 = {'license_expression': ''}
    result1 = filter.include_filtering(input1, include_condition)
    assert result1 == input1
    result2 = filter.include_filtering(input2, include_condition)
    assert result2 == None


def test_and_include_filtering():
    include_condition = [{u'notes': [u'a', u'b']}, {u'Resource': [u'.java']}]
    input1 = {'notes': 'b', 'Resource': '/project/123/'}
    input2 = {'notes': 'b', 'Resource': '/project/123/test.java'}
    result1 = filter.include_filtering(input1, include_condition)
    assert result1 == None
    result2 = filter.include_filtering(input2, include_condition)
    assert result2 == input2


def test_simple_exclude_filtering():
    input = {'notes': 'a', 'Resource': '/project/123/sample1.c'}
    exclude_condition1 = [{u'notes': [u'a']}]
    result1 = filter.exclude_filtering(input, exclude_condition1)
    assert result1 == None
    exclude_condition2 = [{u'notes': [u'b']}]
    result2 = filter.exclude_filtering(input, exclude_condition2)
    assert result2 == input


def test_or_exclude_filtering():
    exclude_condition = [{u'notes': [u'a', u'b'], u'Resource': [u'.java']}]
    input1 = {'notes': 'b', 'Resource': '/project/123/'}
    result1 = filter.exclude_filtering(input1, exclude_condition)
    assert result1 == None
    input2 = {'notes': 'c', 'Resource': '/project/123/'}
    result2 = filter.exclude_filtering(input2, exclude_condition)
    assert result2 == input2


def test_exclude_filtering_with_true_condition():
    exclude_condition = [{u'license_expression': True}]
    input1 = {'license_expression': 'mit'}
    input2 = {'license_expression': ''}
    result1 = filter.exclude_filtering(input1, exclude_condition)
    assert result1 == None
    result2 = filter.exclude_filtering(input2, exclude_condition)
    assert result2 == input2


def test_and_exclude_filtering():
    exclude_condition = [{u'notes': [u'a', u'b']}, {u'Resource': [u'.java']}]
    input1 = {'notes': 'b', 'Resource': '/project/123/'}
    input2 = {'notes': 'b', 'Resource': '/project/123/test.java'}
    input3 = {'notes': 'c', 'Resource': '/project/123/test.c'}
    result1 = filter.exclude_filtering(input1, exclude_condition)
    assert result1 == None
    result2 = filter.exclude_filtering(input2, exclude_condition)
    assert result2 == None
    result3 = filter.exclude_filtering(input3, exclude_condition)
    assert result3 == input3


def test_simple_startswith_filtering():
    input = {'notes': 'a', 'Resource': '/project/123/sample1.c'}
    startswith_condition1 = [{u'notes': [u'a']}]
    result1 = filter.startswith_filtering(input, startswith_condition1)
    assert result1 == input
    startswith_condition2 = [{u'notes': [u'b']}]
    result2 = filter.startswith_filtering(input, startswith_condition2)
    assert result2 == None


def test_or_startswith_filtering():
    startswith_condition = [
        {u'notes': [u'a', u'b'], u'Resource': [u'/project/']}]
    input1 = {'notes': 'b', 'Resource': '/project/123/'}
    result1 = filter.startswith_filtering(input1, startswith_condition)
    assert result1 == input1
    input2 = {'notes': 'c', 'Resource': '/project/123/test.java'}
    result2 = filter.startswith_filtering(input2, startswith_condition)
    assert result2 == input2


def test_and_startswith_filtering():
    startswith_condition = [{u'notes': [u'a', u'b']},
                            {u'Resource': [u'/project/']}]
    input1 = {'notes': 'b', 'Resource': '/project1/123/'}
    input2 = {'notes': 'b', 'Resource': '/project/123/test.java'}
    input3 = {'notes': 'c', 'Resource': '/project2/123/test.java'}
    result1 = filter.startswith_filtering(input1, startswith_condition)
    assert result1 == None
    result2 = filter.startswith_filtering(input2, startswith_condition)
    assert result2 == input2
    result3 = filter.startswith_filtering(input3, startswith_condition)
    assert result3 == None


def test_simple_endswith_filtering():
    input = {'notes': 'a', 'Resource': '/project/123/sample1.c'}
    endswith_condition1 = [{u'Resource': [u'.c']}]
    result1 = filter.endswith_filtering(input, endswith_condition1)
    assert result1 == input


def test_or_endswith_filtering():
    endswith_condition = [{u'notes': [u'a', u'b'], u'Resource': [u'.java']}]
    input1 = {'notes': 'b', 'Resource': '/project/123/'}
    result1 = filter.endswith_filtering(input1, endswith_condition)
    assert result1 == input1
    input2 = {'notes': 'c', 'Resource': '/project/123/test.java'}
    result2 = filter.endswith_filtering(input2, endswith_condition)
    assert result2 == input2


def test_and_endswith_filtering():
    endswith_condition = [{u'notes': [u'a', u'b']}, {u'Resource': [u'.java']}]
    input1 = {'notes': 'b', 'Resource': '/project1/123/'}
    input2 = {'notes': 'b', 'Resource': '/project/123/test.java'}
    input3 = {'notes': 'c', 'Resource': '/project2/123/test.java'}
    result1 = filter.endswith_filtering(input1, endswith_condition)
    assert result1 == None
    result2 = filter.endswith_filtering(input2, endswith_condition)
    assert result2 == input2
    result3 = filter.endswith_filtering(input3, endswith_condition)
    assert result3 == None


def test_simple_equals_filtering():
    input = {'notes': 'a', 'Resource': '/project/123/sample1.c'}
    equals_condition1 = [{u'notes': [u'a']}]
    result1 = filter.equals_filtering(input, equals_condition1)
    assert result1 == input
    equals_condition2 = [{u'notes': [u'b']}]
    result2 = filter.equals_filtering(input, equals_condition2)
    assert result2 == None


def test_or_equals_filtering():
    equals_condition = [{u'notes': [u'a', u'b'], u'Resource': [u'.java']}]
    input1 = {'notes': 'b', 'Resource': '/project/123/'}
    result1 = filter.equals_filtering(input1, equals_condition)
    assert result1 == input1


def test_and_equals_filtering():
    equals_condition = [{u'notes': [u'c', u'b']},
                        {u'Resource': [u'/project1/123/']}]
    input1 = {'notes': 'b', 'Resource': '/project1/123/'}
    input2 = {'notes': 'b', 'Resource': '/project/123/test.java'}
    input3 = {'notes': 'c', 'Resource': '/project2/123/test.java'}
    result1 = filter.equals_filtering(input1, equals_condition)
    assert result1 == input1
    result2 = filter.equals_filtering(input2, equals_condition)
    assert result2 == None
    result3 = filter.equals_filtering(input3, equals_condition)
    assert result3 == None
