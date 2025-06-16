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

from commoncode.testcase import FileBasedTesting
from utilitycode import unicode_to_ascii


class TestDetectUnicode(FileBasedTesting):

    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_check_unicode_not_present(self):
        rows = [{'field1': '10010', 'field2': 'test/test.c'}]
        result, unicode_detected = unicode_to_ascii.check_unicode(rows)
        assert result == rows
        assert not unicode_detected

    def test_check_unicode_present(self):
        rows = [{'field1': 'Eduardo Sánchez Díaz Durán',
                 'field2': 'Copyright © abc'}]
        result, unicode_detected = unicode_to_ascii.check_unicode(rows)
        expected = [{'field1': 'Eduardo Sánchez Díaz Durán', 'field2': 'Copyright © abc',
                     'Unicode Detected': 'x', 'Ignored Unicode - field1': 'Eduardo Sanchez Diaz Duran',
                     'Ignored Unicode - field2': 'Copyright  abc'}]
        assert unicode_detected
        assert result == expected
