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

from utilitycode import analyze_gem


class TestAnalyzeGem():

    def test_get_gem_metadata(self):
        input = [('ffi', '1.15.5')]
        expected = [('ffi', 'v 1.15.5', 'Wayne Meissner',
                     'BSD-3-Clause', 'https://rubygems.org/gems/ffi-1.15.5.gem')]
        output = analyze_gem.get_gem_metadata(input)
        assert expected == output
