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

vocab_list = []


def load_csv(filename, level):
    with open(filename) as csv_file:
        first = True
        csv_reader = csv.reader(csv_file, delimiter=',')
        # index 1 is kanji
        # index 2 is kana
        # index 4 is origin (waller or jmdict)
        for row in csv_reader:
            if first:  # skip first row (headers)
                first = False
                continue
            if row[4] == "waller":
                vocab_level = level
            else:
                vocab_level = -level
            vocab_list.append([row[1], row[2], vocab_level])


load_csv("n5.csv", 5)
load_csv("n4.csv", 4)
load_csv("n3.csv", 3)
load_csv("n2.csv", 2)
load_csv("n1.csv", 1)

if Path("jlpt").is_dir():
    shutil.rmtree("jlpt")
os.mkdir("jlpt")

i = 0
bank = 1
first = True

for vocab in vocab_list:
    with open(f"jlpt/term_meta_bank_{bank}.json", 'a') as f:
        if first:
            f.write('[')
            first = False
        else:
            f.write(',\n')
        if vocab[0] != "":
            f.write(f'["{vocab[0]}","freq"'
                    f',{{"reading":"{vocab[1]}","frequency":{vocab[2]}}}]')
        else:
            f.write(f'["{vocab[1]}","freq",{vocab[2]}]')
        i = i + 1
        if i % 4000 == 0 or i == len(vocab_list):
            f.write(']')
            first = True
            bank = bank + 1

with open("jlpt/index.json", 'w') as f:
    f.write('{"revision":"JLPT;2021-10-14"'
            ',"description":"https://github.com/stephenmk/yomichan-jlpt-vocab"'
            ',"title":"JLPT"'
            ',"format":3'
            ',"author":"stephenmk"}')
