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

vocab = {}


def load_csv(filename, level):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # index 0 is kanji
        # index 1 is kana
        for row in csv_reader:
            if row[0] == "":
                key = row[1]
            else:
                key = (row[0], row[1])
            if key not in vocab:
                vocab[key] = level
            else:
                # it's a duplicate
                pass


load_csv("n5.csv", "N5")
load_csv("n4.csv", "N4")
load_csv("n3.csv", "N3")
load_csv("n2.csv", "N2")
load_csv("n1.csv", "N1")

if Path("jlpt").is_dir():
    shutil.rmtree("jlpt")
os.mkdir("jlpt")

i = 0
bank = 1
first = True

for key in vocab:
    with open(f"jlpt/term_meta_bank_{bank}.json", 'a') as f:
        if first:
            f.write('[')
            first = False
        else:
            f.write(',')
        if type(key) == tuple:
            f.write(f'["{key[0]}","freq"'
                    f',{{"reading":"{key[1]}","frequency":"{vocab[key]}"}}]')
        else:
            f.write(f'["{key}","freq","{vocab[key]}"]')
        i = i + 1
        if i % 4000 == 0 or i == len(vocab):
            f.write(']')
            first = True
            bank = bank + 1

with open("jlpt/index.json", 'w') as f:
    f.write('{"revision":"JLPT;2021-09-04"'
            ',"description":"https://github.com/stephenmk/yomichan-jlpt-vocab"'
            ',"title":"JLPT"'
            ',"format":3'
            ',"author":"stephenmk"}')
