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

from collections import defaultdict

import io
import json
import os

from click.testing import CliRunner
import unicodecsv

from commoncode.testcase import FileBasedTesting
from utilitycode import system_file_index


class TestSystemFileIndex(FileBasedTesting):

    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_system_file_index_get_matches(self):
        packages_by_path = defaultdict(list)
        packages_by_path['bin/busybox'].append('busybox')
        paths = ['/foo/bar/bin/bin/busybox']
        results = list(system_file_index.get_matches(paths, packages_by_path))
        self.assertEqual(1, len(results))
        result = results[0]
        matched_path = result.path
        matched_suffix = result.matched_suffix
        package = result.matched_package
        expected_path = '/foo/bar/bin/bin/busybox'
        expected_suffix = 'bin/busybox'
        expected_package = 'busybox'
        self.assertEqual(expected_path, matched_path)
        self.assertEqual(expected_suffix, matched_suffix)
        self.assertEqual(expected_package, package)

    def test_system_file_index_parse_contents(self):
        truncated_contents_file = self.get_test_loc(
            'system_file_index/truncated-contents-file.gz')
        packages_by_path, paths_by_packages = system_file_index.parse_contents(
            truncated_contents_file)
        expected_packages_by_path = self.get_test_loc(
            'system_file_index/expected-packages-by-path.json')
        check_json(packages_by_path, expected_packages_by_path, regen=False)
        expected_paths_by_packages = self.get_test_loc(
            'system_file_index/expected-paths-by-packages.json')
        check_json(paths_by_packages, expected_paths_by_packages, regen=False)

    def test_system_file_index_cli(self):
        test_index_file = self.get_test_loc(
            'system_file_index/test-index-file')
        test_csv = self.get_test_loc('system_file_index/test-in.csv')
        output_csv = self.get_temp_file('test-out.csv')
        expected_csv = self.get_test_loc('system_file_index/expected.csv')
        options = ['--index-file', test_index_file, test_csv, output_csv]
        runner = CliRunner()
        _ = runner.invoke(system_file_index.cli, options,
                          catch_exceptions=False)
        check_csvs(output_csv, expected_csv, regen=False)


def check_json(result, expected_file, regen=False):
    if regen:
        with open(expected_file, 'wb') as reg:
            reg.write(
                json.dumps(
                    result,
                    indent=4,
                    separators=(',', ': '),
                    ensure_ascii=False
                ).encode('utf-8')
            )
    with io.open(expected_file, encoding='utf-8') as exp:
        expected = json.load(exp, object_pairs_hook=dict)
    assert expected == result


def load_csv(location):
    """
    Load a CSV file at location and return a tuple of (field names, list of rows as
    mappings field->value).
    """
    with io.open(location, 'rb') as csvin:
        reader = unicodecsv.DictReader(csvin)
        fields = reader.fieldnames
        values = sorted(reader, key=lambda d: d.items())
        return fields, values


def check_csvs(result_file, expected_file,
               ignore_keys=('date', 'file_type', 'mime_type',),
               regen=False):
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
    for exp, res in zip(sorted(expected, key=lambda d: d.items()), sorted(results, key=lambda d: d.items())):
        for ign in ignore_keys:
            exp.pop(ign, None)
            res.pop(ign, None)
        assert exp == res
