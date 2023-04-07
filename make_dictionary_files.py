#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2021-2023 Stephen Kraus
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


def make_jlpt_freq(level, origin, original):
    freq_value = level
    if origin == "waller":
        freq_display = f"N{level}"
    elif origin == "jmdict":
        freq_display = f"N{level} ({original})"
    else:
        raise Exception(f"Unexpected 'origin' in N{level} data: '{origin}'")
    freq = {
        "value":        freq_value,
        "displayValue": freq_display
    }
    return freq


def row_to_jlpt_term(row, level):
    (_, kanji, kana, _, origin, original) = row
    freq = make_jlpt_freq(level, origin, original)
    if kanji != "":
        term = [kanji, "freq", {"reading": kana, "frequency": freq}]
    else:
        term = [kana, "freq", freq]
    return term


def load_csv(filepath):
    csv_data = []
    with open(filepath) as csv_file:
        first = True
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if first:  # skip first row (headers)
                first = False
                continue
            csv_data.append(row)
    return csv_data


def make_jlpt_terms():
    terms = []
    for jlpt_level in [5, 4, 3, 2, 1]:
        filepath = os.path.join("data", f"n{jlpt_level}.csv")
        csv_data = load_csv(filepath)
        for row in csv_data:
            term = row_to_jlpt_term(row, jlpt_level)
            terms.append(term)
    return terms


def write_term_meta_dictionary(terms, filename, index):
    output_dir = str(uuid.uuid4())
    os.mkdir(output_dir)

    terms_per_file = 4000
    max_i = int(len(terms) / terms_per_file) + 1
    for i in range(max_i):
        term_file = os.path.join(output_dir, f"term_meta_bank_{i+1}.json")
        with open(term_file, "w", encoding='utf8') as f:
            start = terms_per_file * i
            end = terms_per_file * (i + 1)
            json.dump(terms[start:end], f, indent=4, ensure_ascii=False)

    index_file = os.path.join(output_dir, "index.json")
    with open(index_file, 'w') as f:
        json.dump(index, f, indent=4, ensure_ascii=False)

    if Path(f"{filename}.zip").is_file():
        os.remove(f"{filename}.zip")

    shutil.make_archive(filename, 'zip', output_dir)
    shutil.rmtree(output_dir)


if __name__ == '__main__':
    terms = make_jlpt_terms()
    filename = "jlpt"
    index = {
        "revision":    "JLPT;2022-01-30",
        "description": "https://github.com/stephenmk/yomichan-jlpt-vocab",
        "title":       "JLPT",
        "format":      3,
        "author":      "stephenmk",
    }
    write_term_meta_dictionary(terms, filename, index)
