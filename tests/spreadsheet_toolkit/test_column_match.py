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

import io
import os

from click.testing import CliRunner
from commoncode.testcase import FileBasedTesting
import unicodecsv

from spreadsheet_toolkit import column_match
from spreadsheet_toolkit.csv_utils import read_csv_rows


def load_csv(location):
    """
    Load a CSV file at location and return a tuple of (field names, list of rows as
    mappings field->value).
    """
    with io.open(location, "rb") as csvin:
        reader = unicodecsv.DictReader(csvin)
        fields = reader.fieldnames
        values = sorted(reader, key=lambda d: d.items())
        return fields, values


def check_csvs(
    result_file,
    expected_file,
    ignore_keys=(
        "date",
        "file_type",
        "mime_type",
    ),
    regen=False,
):
    """
    Load and compare two CSVs.
    `ignore_keys` is a tuple of keys that will be ignored in the comparisons.
    """
    result_fields, results = load_csv(result_file)
    if regen:
        import shutil

        shutil.copy2(result_file, expected_file)
    expected_fields, expected = load_csv(expected_file)
    assert expected_fields == result_fields
    # then check results line by line for more compact results
    for exp, res in zip(
        sorted(expected, key=lambda d: d.items()),
        sorted(results, key=lambda d: d.items()),
    ):
        for ign in ignore_keys:
            exp.pop(ign, None)
            res.pop(ign, None)
        assert exp == res


def check_results(results, expected_results):
    """
    Assert whether or not every item in `results` is in `expected_results`
    """
    assert len(results) == len(expected_results)
    for item in results:
        assert item in expected_results


class TestColumnMatch(FileBasedTesting):
    test_data_dir = os.path.join(os.path.dirname(__file__), "data")
    input1 = [
        {"Resource": "/tmp/test.c", "license_expression": "mit", "type": "file"},
        {
            "Resource": "/tmp/include/test.h",
            "license_expression": "public-domain",
            "type": "file",
        },
        {
            "Resource": "/tmp/include/test.cc",
            "license_expression": "apache-2.0",
            "type": "file",
        },
    ]
    input2 = [
        {"Resource": "/test.c", "license_expression": "mit-2", "note": ""},
        {
            "Resource": "/tmp/include/test.h",
            "license_expression": "public-domain-2",
            "note": "NOTE",
        },
        {
            "Resource": "/tmp/test.c",
            "license_expression": "public-domain-3",
            "note": "NOTE",
        },
    ]
    input3 = [
        {"Resource": "/test.c", "license_expression": "mit-2", "note": ""},
        {
            "Resource": "/tmp/include/test.h",
            "license_expression": "public-domain-2",
            "note": "NOTE",
        },
        {
            "Resource": "/tmp/test.c",
            "license_expression": "public-domain-3",
            "note": "NOTE",
        },
        {
            "Resource": "/tmp/test.c",
            "license_expression": "apache-2.0",
            "note": "OTHER NOTE",
        },
    ]
    headers1 = ["Resource", "license_expression", "type"]
    headers2 = ["Resource", "license_expression", "note"]
    key1 = "Resource"
    key2 = "Resource"

    def test_get_rows_by_split_resolved_path(self):
        results = list(
            column_match.get_rows_by_split_resolved_path(
                result1=self.input1, key1=self.key1
            )
        )
        expected_results = [
            (
                "test.c",
                ("test.c", "tmp"),
                {
                    "Resource": "/tmp/test.c",
                    "license_expression": "mit",
                    "type": "file",
                    "resolved_Resource": "tmp/test.c",
                },
            ),
            (
                "test.h",
                ("test.h", "include", "tmp"),
                {
                    "Resource": "/tmp/include/test.h",
                    "license_expression": "public-domain",
                    "type": "file",
                    "resolved_Resource": "tmp/include/test.h",
                },
            ),
            (
                "test.cc",
                ("test.cc", "include", "tmp"),
                {
                    "Resource": "/tmp/include/test.cc",
                    "license_expression": "apache-2.0",
                    "type": "file",
                    "resolved_Resource": "tmp/include/test.cc",
                },
            ),
        ]
        self.assertEqual(results, expected_results)

    def test_get_rows_by_split_resolved_path_by_filename(self):
        results = column_match.get_rows_by_split_resolved_path_by_filename(
            results2=self.input3, key2=self.key2
        )
        expected_results = {
            'test.c': {
                ('test.c',): [
                    {
                        'Resource': '/test.c',
                        'license_expression': 'mit-2',
                        'note': '',
                        'resolved_Resource': 'test.c'
                    }
                ],
                ('test.c', 'tmp'): [
                    {
                        'Resource': '/tmp/test.c',
                        'license_expression': 'public-domain-3',
                        'note': 'NOTE',
                        'resolved_Resource': 'tmp/test.c'
                    },
                    {
                        'Resource': '/tmp/test.c',
                        'license_expression': 'apache-2.0',
                        'note': 'OTHER NOTE',
                        'resolved_Resource': 'tmp/test.c'
                    }
                ]
            },
            'test.h': {
                ('test.h', 'include', 'tmp'): [
                    {
                        'Resource': '/tmp/include/test.h',
                        'license_expression': 'public-domain-2',
                        'note': 'NOTE',
                        'resolved_Resource': 'tmp/include/test.h'
                    }
                ]
            }
        }
        self.assertEqual(results, expected_results)

    def test_generate_headers(self):
        headers = column_match.generate_headers(self.headers1, self.headers2, self.key2)
        expected_headers = [
            "Resource",
            "license_expression",
            "type",
            "resolved_Resource",
            "matched",
            "matched_score_from_right",
            "matched_score_from_left",
            "total_path_segments_count",
            "match_percentage_from_right",
            "match_percentage_from_left",
            "matched_Resource",
            "matched_license_expression",
            "note",
        ]
        self.assertEqual(headers, expected_headers)

    def test_column_match(self):
        results = list(
            column_match.column_match(
                result1=self.input1,
                result2=self.input2,
                headers1=self.headers1,
                headers2=self.headers2,
                key1=self.key1,
                key2=self.key2,
            )
        )
        expected_results = [
            {
                "Resource": "/tmp/test.c",
                "license_expression": "mit",
                "type": "file",
                "resolved_Resource": "tmp/test.c",
                "matched": "test.c",
                "matched_score_from_right": 1,
                "total_path_segments_count": 2,
                "match_percentage_from_right": 50.0,
                "matched_Resource": "/test.c",
                "matched_license_expression": "mit-2",
                "note": "",
                "matched_score_from_left": 1,
                "match_percentage_from_left": 50.0,
            },
            {
                "Resource": "/tmp/test.c",
                "license_expression": "mit",
                "type": "file",
                "resolved_Resource": "tmp/test.c",
                "matched": "tmp/test.c",
                "matched_score_from_right": 2,
                "total_path_segments_count": 2,
                "match_percentage_from_right": 100.0,
                "matched_Resource": "/tmp/test.c",
                "matched_license_expression": "public-domain-3",
                "note": "NOTE",
                "matched_score_from_left": 2,
                "match_percentage_from_left": 100.0,
            },
            {
                "Resource": "/tmp/include/test.h",
                "license_expression": "public-domain",
                "type": "file",
                "resolved_Resource": "tmp/include/test.h",
                "matched": "tmp/include/test.h",
                "matched_score_from_right": 3,
                "total_path_segments_count": 3,
                "match_percentage_from_right": 100.0,
                "matched_Resource": "/tmp/include/test.h",
                "matched_license_expression": "public-domain-2",
                "note": "NOTE",
                "matched_score_from_left": 3,
                "match_percentage_from_left": 100.0,
            },
            {
                "Resource": "/tmp/include/test.cc",
                "license_expression": "apache-2.0",
                "type": "file",
                "resolved_Resource": "tmp/include/test.cc",
            },
        ]
        check_results(results, expected_results)

    def test_column_match_best_matches_only(self):
        results = list(
            column_match.column_match(
                result1=self.input1,
                result2=self.input2,
                headers1=self.headers1,
                headers2=self.headers2,
                key1=self.key1,
                key2=self.key2,
                best_matches_only=True,
            )
        )
        expected_results = [
            {
                "Resource": "/tmp/test.c",
                "license_expression": "mit",
                "type": "file",
                "resolved_Resource": "tmp/test.c",
                "matched": "tmp/test.c",
                "matched_score_from_right": 2,
                "total_path_segments_count": 2,
                "match_percentage_from_right": 100.0,
                "matched_Resource": "/tmp/test.c",
                "matched_license_expression": "public-domain-3",
                "note": "NOTE",
                "matched_score_from_left": 2,
                "match_percentage_from_left": 100.0,
            },
            {
                "Resource": "/tmp/include/test.h",
                "license_expression": "public-domain",
                "type": "file",
                "resolved_Resource": "tmp/include/test.h",
                "matched": "tmp/include/test.h",
                "matched_score_from_right": 3,
                "total_path_segments_count": 3,
                "match_percentage_from_right": 100.0,
                "matched_Resource": "/tmp/include/test.h",
                "matched_license_expression": "public-domain-2",
                "note": "NOTE",
                "matched_score_from_left": 3,
                "match_percentage_from_left": 100.0,
            },
            {
                "Resource": "/tmp/include/test.cc",
                "license_expression": "apache-2.0",
                "type": "file",
                "resolved_Resource": "tmp/include/test.cc",
            },
        ]
        check_results(results, expected_results)

    def test_column_match_multiple_rows_for_same_resource_in_input2(self):
        input3 = [
            {"Resource": "/test.c", "license_expression": "mit-2", "note": ""},
            {
                "Resource": "/tmp/include/test.h",
                "license_expression": "public-domain-2",
                "note": "NOTE",
            },
            {
                "Resource": "/tmp/test.c",
                "license_expression": "public-domain-3",
                "note": "NOTE",
            },
            {
                "Resource": "/tmp/test.c",
                "license_expression": "apache-2.0",
                "note": "OTHER NOTE",
            },
        ]
        results = list(
            column_match.column_match(
                result1=self.input1,
                result2=input3,
                headers1=self.headers1,
                headers2=self.headers2,
                key1=self.key1,
                key2=self.key2,
                best_matches_only=True,
            )
        )
        expected_results = [
            {
                "Resource": "/tmp/test.c",
                "license_expression": "mit",
                "type": "file",
                "resolved_Resource": "tmp/test.c",
                "matched": "tmp/test.c",
                "matched_score_from_right": 2,
                "total_path_segments_count": 2,
                "match_percentage_from_right": 100.0,
                "matched_Resource": "/tmp/test.c",
                "matched_license_expression": "public-domain-3",
                "note": "NOTE",
                "matched_score_from_left": 2,
                "match_percentage_from_left": 100.0,
            },
            {
                "Resource": "/tmp/test.c",
                "license_expression": "mit",
                "type": "file",
                "resolved_Resource": "tmp/test.c",
                "matched": "tmp/test.c",
                "matched_score_from_right": 2,
                "total_path_segments_count": 2,
                "match_percentage_from_right": 100.0,
                "matched_Resource": "/tmp/test.c",
                "matched_license_expression": "apache-2.0",
                "note": "OTHER NOTE",
                "matched_score_from_left": 2,
                "match_percentage_from_left": 100.0,
            },
            {
                "Resource": "/tmp/include/test.h",
                "license_expression": "public-domain",
                "type": "file",
                "resolved_Resource": "tmp/include/test.h",
                "matched": "tmp/include/test.h",
                "matched_score_from_right": 3,
                "total_path_segments_count": 3,
                "match_percentage_from_right": 100.0,
                "matched_Resource": "/tmp/include/test.h",
                "matched_license_expression": "public-domain-2",
                "note": "NOTE",
                "matched_score_from_left": 3,
                "match_percentage_from_left": 100.0,
            },
            {
                "Resource": "/tmp/include/test.cc",
                "license_expression": "apache-2.0",
                "type": "file",
                "resolved_Resource": "tmp/include/test.cc",
            },
        ]
        check_results(results, expected_results)

    def test_column_match_end_to_end(self):
        test_csv = self.get_test_loc("column_match/input_1.csv")
        test_csv_2 = self.get_test_loc("column_match/input_2.csv")
        output_csv = self.get_temp_file("out.csv")
        expected_csv = self.get_test_loc("column_match/expected.csv")
        options = [
            "-k1",
            "dwarf_source_path",
            "-k2",
            "Resource",
            test_csv,
            test_csv_2,
            output_csv,
            "--csv"
        ]
        runner = CliRunner()
        _ = runner.invoke(column_match.cli, options, catch_exceptions=False)
        output = read_csv_rows(output_csv)
        expected = read_csv_rows(expected_csv)
        assert list(output) == list(expected)
        #check_csvs(output_csv, expected_csv, regen=False)
