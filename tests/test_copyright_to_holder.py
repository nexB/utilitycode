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

from commoncode.testcase import FileBasedTesting
from utilitycode import copyright_to_holder


class TestCopyrightToHolder(FileBasedTesting):

    def test_convert_copyright_to_holder_simple(self):
        simple_copyright = "Copyright (c) nexB, Inc."
        expected = "nexB, Inc."
        result = copyright_to_holder.convert_copyright_to_holder(
            simple_copyright)
        assert result == expected

    def test_convert_copyright_to_holder_multiple(self):
        multi_copyright = """
Copyright (c) nexB, Inc.
Copyright (c) ABC
1995-2017 Jean-loup Gailly
1995-2017 Mark Adler
"""
        expected = "nexB, Inc., ABC, Jean-loup Gailly, Mark Adler"
        result = copyright_to_holder.convert_copyright_to_holder(
            multi_copyright)
        assert result == expected
