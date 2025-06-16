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

from utilitycode import json_to_xlsx
import pytest


class TestAnalyzeGem():

    def test_json_to_xlsx(self):
        input = [
            {
                "purl": "pkg:pypi/six@1.16.0",
                "dependents_count": "88550"
            },
            {
                "purl": "pkg:pypi/idna@3.6.0",
                "dependents_count": "87737"
            }
        ]
        expected_headers = ["purl", "dependents_count"]
        expected_rows = [["pkg:pypi/six@1.16.0", "88550"],
                         ["pkg:pypi/idna@3.6.0", "87737"]]
        headers, rows = json_to_xlsx.json_to_xlsx(input)
        assert expected_headers == headers
        assert expected_rows == rows

    def test_json_to_xlsx_unmatched_elements(self):
        input = [
            {
                "purl": "pkg:pypi/six@1.16.0",
            },
            {
                "purl": "pkg:pypi/idna@3.6.0",
                "dependents_count": "87737"
            }
        ]
        expected_headers = ["purl", "dependents_count"]
        expected_rows = [["pkg:pypi/six@1.16.0", ""],
                         ["pkg:pypi/idna@3.6.0", "87737"]]
        headers, rows = json_to_xlsx.json_to_xlsx(input)
        assert expected_headers == headers
        assert expected_rows == rows

    def test_json_to_xlsx_unmatched_elements2(self):
        input = [
            {
                "purl": "pkg:pypi/six@1.16.0",
            },
            {
                "purl": "pkg:pypi/idna@3.6.0",
                "dependents_count": "87737"
            },
            {
                "purl": "pkg:pypi/idna",
                "license": "bsd-new"
            }
        ]
        expected_headers = ["purl", "dependents_count", "license"]
        expected_rows = [["pkg:pypi/six@1.16.0", "", ""],
                         ["pkg:pypi/idna@3.6.0", "87737", ""],
                         ["pkg:pypi/idna", "", "bsd-new"]]
        headers, rows = json_to_xlsx.json_to_xlsx(input)
        assert expected_headers == headers
        assert expected_rows == rows

    def test_json_to_xlsx_not_list_of_dict(self):
        input = {"purl": "pkg:pypi/six@1.16.0"}
        with pytest.raises(
                ValueError,
                match="JSON format must be a list of dictionaries."):
            json_to_xlsx.json_to_xlsx(input)
