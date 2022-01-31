#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2021 Stephen Kraus
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pathlib import Path
import csv
import os
import shutil
import json
import uuid


def convert_csv_to_json(row, level):
    kanji, kana, origin, original = [row[i] for i in (1, 2, 4, 5)]
    freq_value = level
    if origin == "waller":
        freq_display = f"N{level}"
    elif origin == "jmdict":
        freq_display = f"N{level} ({original})"
    else:
        raise Exception(f"Unexpected 'origin' in N{level} data: '{origin}'")
    if kanji != "":
        entry = [kanji, "freq", {"reading": kana, "frequency": {
            "value": freq_value, "displayValue": freq_display}}]
    else:
        entry = [kana, "freq", {"value": freq_value,
                                "displayValue": freq_display}]
    json_string = json.dumps(entry, ensure_ascii=False)
    return json_string


def load_csv(filename):
    csv_data = []
    with open(filename) as csv_file:
        first = True
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if first:  # skip first row (headers)
                first = False
                continue
            csv_data.append(row)
    return csv_data


dictionary_entries = []

for jlpt_level in [5, 4, 3, 2, 1]:
    filename = f"n{jlpt_level}.csv"
    csv_data = load_csv(filename)
    for row in csv_data:
        entry = convert_csv_to_json(row, jlpt_level)
        dictionary_entries.append(entry)

output_dir = f"jlpt-{uuid.uuid4()}"
os.mkdir(output_dir)

i = 0
bank = 1
first = True

for entry in dictionary_entries:
    with open(f"{output_dir}/term_meta_bank_{bank}.json", 'a') as f:
        if first:
            f.write('[')
            first = False
        else:
            f.write(',\n')
        f.write(entry)
        i = i + 1
        if i % 4000 == 0 or i == len(dictionary_entries):
            f.write(']')
            first = True
            bank = bank + 1

with open(f"{output_dir}/index.json", 'w') as f:
    f.write('{"revision":"JLPT;2022-01-30"'
            ',"description":"https://github.com/stephenmk/yomichan-jlpt-vocab"'
            ',"title":"JLPT"'
            ',"format":3'
            ',"author":"stephenmk"}')

if Path("jlpt.zip").is_file():
    os.remove("jlpt.zip")

shutil.make_archive("jlpt", 'zip', output_dir)
shutil.rmtree(output_dir)
