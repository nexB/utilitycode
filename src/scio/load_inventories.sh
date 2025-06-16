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

# Creating SCIO Projects for JSON Files in a Directory.
# The project name will be the file basename.

# Example:
# ./load_inventories.sh <scio_repo_path or scio_installed_path> <input_directory_path_with_set_of_jsons>
# ./load_inventories.sh /tools/scancode.io /projects/scans/

# Note:
# The following code runs the `load_inventory`` pipeline. Replace the pipeline name as needed.

# Check if the script has exactly two arguments
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 scio_path input_path"
  exit 1
fi

scio_dir=$1
directory=$2

# Check if the SCIO directory exists
if [ ! -d "$scio_dir" ]; then
  echo "SCIO Directory $scio_dir does not exist."
  exit 1
fi

# Check if the directory exists
if [ ! -d "$directory" ]; then
  echo "Directory $directory does not exist."
  exit 1
fi


# Walk through the directory and process files
files=$(find "$directory" -type f \( -name "*.json" -o -name "*.xlsx" \))

for file in $files; do
  echo "Processing $file"
  filename=$(basename "$file")
  basename="${filename%.*}"
  #basename="${filename%%@*}"

  # Execute the load_inventory pipeline
  docker compose -f $scio_dir/docker-compose.yml run -T --volume "$directory:$directory:ro" web scanpipe create-project "$basename" \
    --input-file "$file" \
    --pipeline load_inventory \
    --execute
done


echo "Finished."
