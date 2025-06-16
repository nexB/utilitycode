#!/usr/bin/env python
# -*- coding: utf8 -*-

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

from collections import defaultdict
from difflib import SequenceMatcher
import click
import sys

from commoncode.paths import resolve

from spreadsheet_toolkit.csv_utils import get_csv_headers, read_csv_rows
from utilitycode.bom_utils import get_data_from_xlsx
from utilitycode.bom_utils import write_to_csv
from utilitycode.bom_utils import write_to_xlsx


def get_rows_by_split_resolved_path(result1, key1):
    """
    Yield a tuple of file name, reversed path segments, and row from `result1`.

    `result1` is a list of dictionaries, where each dictionary contains the
    information of a CSV row.

    `key1` is the key whose value is the path to be
    matched against.

    The file name and reversed path segments that are returned in the tuple are
    determined by getting the value for `key1` (which is a path string) from a
    dictionary within `result1`, resolving the `key1` path (removing ".",
    resolving "..", within file paths), splitting the path into segments, and
    returning it in the reverse order in our tuple. The path segments are
    reversed in order to help us perform path segment matching easier by having
    the leading element be the filename.
    """
    for row in result1:
        key1_val = row[key1]
        path = resolve(key1_val)
        split_path = tuple(reversed(path.split('/')))
        row['resolved_' + key1] = path
        # Sometimes there are headers with no values, this may cause issues when writing the row to csv
        row.pop(None, '')
        row.pop('', '')
        yield split_path[0], split_path, row


def get_rows_by_split_resolved_path_by_filename(results2, key2):
    """
    Return a dictionary of dictionaries that is first organized by filename,
    then by the tuple of resolved path segments (whose order is reversed)

    Each value in the dictionary is a dictionary that contains the CSV row information
    from `results2`.

    The filename and path segments used for organization is determined by `key2`
    """
    rows_by_split_resolved_path_by_filename = defaultdict(
        lambda: defaultdict(list))
    for filename, split_path, row in get_rows_by_split_resolved_path(results2, key2):
        rows_by_split_resolved_path_by_filename[filename][split_path].append(
            row)
    return rows_by_split_resolved_path_by_filename


def generate_headers(headers1, headers2, key1):
    """
    Return a list of strings that are header names for the output of column_match.

    New columns, that deal with the path matching results, are added to `headers1`,
    then the headers from `headers2` are added.

    If there is a header from `headers2` that is named the same as a header from
    `headers1`, we prepend "matched_" to the value of the header from `header2`.
    """
    output_headers = headers1[:]
    output_headers.append('resolved_' + key1)
    output_headers.append('matched')
    output_headers.append('matched_score_from_right')
    output_headers.append('matched_score_from_left')
    output_headers.append('total_path_segments_count')
    output_headers.append('match_percentage_from_right')
    output_headers.append('match_percentage_from_left')
    for header in headers2:
        if header in headers1:
            matched_header = 'matched_' + header
            output_headers.append(matched_header)
        else:
            output_headers.append(header)
    return output_headers


def column_match(result1, result2, headers1, headers2, key1, key2, best_matches_only=False):
    """
    'matched_score' is calculated by the common trailing paths/values between two inputs columns.
    Note: Everything in result1 will be kept even if there is no match.
    """
    # Create index of Resources to match against using `result2`
    result2_rows_by_split_path_by_filename = get_rows_by_split_resolved_path_by_filename(
        result2, key2)

    col_match_results_by_split_path_s1 = defaultdict(lambda: defaultdict(list))
    for file_name, split_path_s1, row1 in get_rows_by_split_resolved_path(result1, key1):
        # We check to see if we have a Resource in result2 that has the same
        # file name as the Resource we are looking at now in result1
        matched_rows_by_split_path = result2_rows_by_split_path_by_filename.get(
            file_name, {})
        if not matched_rows_by_split_path:
            # If there is no Resource with `file_name` in `result2`,
            # append the row to match results without attempting to perform path matching
            # This is a column match result with no score. A non-match is indicated by
            # a score of 0 or no value for score.
            col_match_results_by_split_path_s1[split_path_s1][0].append(row1)
            continue

        s1_size = len(split_path_s1)
        for split_path_s2, matched_rows in matched_rows_by_split_path.items():
            score = 0
            for path_segment_s1, path_segment_s2 in zip(split_path_s1, split_path_s2):
                if path_segment_s1 != path_segment_s2:
                    break
                score += 1

            for matched_row in matched_rows:
                # Calculate match statistics and populate fields
                result_row = row1.copy()
                result_row['matched'] = matched_row['resolved_' + key2]
                result_row['matched_score_from_right'] = score
                result_row['total_path_segments_count'] = s1_size
                column_match_percentage = (score / s1_size) * 100
                result_row['match_percentage_from_right'] = column_match_percentage

                # Carry over values from the matched row to the row we are matching for
                for header in headers2:
                    if header in headers1:
                        matched_header = 'matched_' + header
                        result_row[matched_header] = matched_row[header]
                    else:
                        result_row[header] = matched_row[header]

                # Store matched row
                s1_results = col_match_results_by_split_path_s1[split_path_s1]
                score_s1_results = s1_results[score]
                if result_row in score_s1_results:
                    continue
                score_s1_results.append(result_row)

    if best_matches_only:
        # Keep only the best results, the matches with the highest score
        for path_segs, col_match_results_by_score in col_match_results_by_split_path_s1.items():
            highest_score = max(
                score for score in col_match_results_by_score.keys())
            best_matches = col_match_results_by_split_path_s1[path_segs][highest_score]
            col_match_results_by_split_path_s1[path_segs] = {
                highest_score: best_matches}

    # If we have more than one row for a result, use SequenceMatcher to determine best one,
    # then add the best results to `results`
    # If 'best_matches_only' is true, then only the highest scoring matches will be
    # yielded. Otherwise, all results are yielded.
    for path_segs, col_match_results_by_score in col_match_results_by_split_path_s1.items():
        # `path_segs` is a tuple of reversed path segments, where the first
        # element is the file name, working backwards to the root
        # We reverse `path_segs` so we can sequence match it properly with
        # the path of the matched rows
        path_segs = tuple(reversed(path_segs))
        highest_segment_match_count = 0
        best_segment_match_rows = []
        for score, col_match_results in col_match_results_by_score.items():
            for row in col_match_results:
                matched_path = row.get('matched', '')
                if not matched_path:
                    yield row
                    continue

                # Calculate the number of matching path segments from the beginning of the path
                matched_path_segs = matched_path.split('/')
                seq_matcher = SequenceMatcher(a=path_segs, b=matched_path_segs)
                matching_segments_count = sum(
                    m.size for m in seq_matcher.get_matching_blocks())

                # Write stats to row
                row['matched_score_from_left'] = matching_segments_count
                total_path_segment_count = row.get(
                    'total_path_segments_count', 0)
                if total_path_segment_count:
                    row['match_percentage_from_left'] = (
                        matching_segments_count / total_path_segment_count) * 100

                if best_matches_only:
                    # If `best_matches_only` is True, we want to keep only the best matches
                    # by keeping the row with the highest matching segment count
                    if matching_segments_count > highest_segment_match_count:
                        highest_segment_match_count = matching_segments_count
                        best_segment_match_rows = [row]
                    elif matching_segments_count == highest_segment_match_count:
                        if row in best_segment_match_rows:
                            continue
                        best_segment_match_rows.append(row)
                else:
                    # If `best_matches_only` is False, we want to yield every row
                    yield row

        if best_matches_only:
            # We yield all the best matches after keeping and tracking them
            for row in best_segment_match_rows:
                yield row


@click.command()
@click.option('--best_matches_only',
              required=False,
              metavar='best_matches_only',
              is_flag=True,
              default=False,
              help='Return only the highest scoring matches. '
              'If no match is available for a row from INPUT1, '
              'then that row is returned in OUTPUT with no match result added.')
@click.option('--csv',
              is_flag=True,
              help='Output as CSV format (Default: XLSX format)')
@click.option('-k1', '--key1',
              required=True,
              metavar='key1',
              help='Column name from INPUT1 for matching.')
@click.option('-k2', '--key2',
              required=True,
              metavar='key2',
              help='Column name from INPUT2 for matching.')
@click.argument('input1',
                required=True,
                metavar='INPUT1',
                type=click.Path(
                    exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True))
@click.argument('input2',
                required=True,
                metavar='INPUT2',
                type=click.Path(
                    exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True))
@click.argument('output',
                required=True,
                metavar='OUTPUT',
                type=click.Path(exists=False, dir_okay=False, writable=True, resolve_path=True))
@click.help_option('-h', '--help')
def cli(best_matches_only, csv, key1, key2, input1, input2, output):
    """
    Get the header keys from both input.
    """
    if not input1.endswith('.csv') and not input1.endswith('.xlsx'):
        raise click.UsageError(
            'ERROR: "The input1 does not ends with \'.csv\' or \'.xlsx\' extension.')
    if not input2.endswith('.csv') and not input2.endswith('.xlsx'):
        raise click.UsageError(
            'ERROR: "The input2 does not ends with \'.csv\' or \'.xlsx\' extension.')

    if input1.endswith('.csv'):
        headers1 = get_csv_headers(input1)
        result1 = read_csv_rows(input1)
    else:
        result1, headers1 = get_data_from_xlsx(input1)

    if key1 not in headers1:
        print(key1 + " is not in the INPUT1. Please correct and re-run.")
        sys.exit(1)

    if input2.endswith('.csv'):
        headers2 = get_csv_headers(input2)
        result2 = read_csv_rows(input2)
    else:
        result2, headers2 = get_data_from_xlsx(input2)

    if key2 not in headers2:
        print(key2 + " is not in the INPUT2. Please correct and re-run.")
        sys.exit(1)

    output_headers = generate_headers(
        headers1=headers1,
        headers2=headers2,
        key1=key1
    )

    results = list(column_match(result1, result2, headers1,
                   headers2, key1, key2, best_matches_only))

    # Reorder the result dictionary
    updated_results = []
    for result in results:
        dict = {}
        for header in output_headers:
            try:
                dict[header] = result[header]
            except:
                dict[header] = ''
        updated_results.append(dict)

    if csv:
        if not output.endswith('.csv'):
            raise click.UsageError(
                'ERROR: "The output does not ends with \'.csv\' extension.')
        else:
            write_to_csv(updated_results, output)
    else:
        if not output.endswith('.xlsx'):
            raise click.UsageError(
                'ERROR: "The output does not ends with \'.xlsx\' extension.')
        else:
            write_to_xlsx(updated_results, output)
