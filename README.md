# yomitan-jlpt-vocab

This meta dictionary adds
[JLPT-level](https://www.jlpt.jp/e/about/levelsummary.html) tags to
words in [Yomitan](https://yomitan.wiki/).

![N5 tag on the word 読む](img/example.png)

## Attribution

JLPT data is sourced from [Jonathan Waller‘s](http://www.tanos.co.uk/contact/)
[JLPT Resources](http://www.tanos.co.uk/jlpt/) page under the terms of the
Creative Commons BY license. This is the same resource used by
[jisho](https://jisho.org/), so the information found there should be
roughly equivalent.

For each word on Waller's lists, I have added an entry ID for the
corresponding entry in the
[JMDict](https://www.edrdg.org/jmdict/j_jmdict.html) database. I have
used data from JMdict to inspect every word and determine which
spellings of particular words are most common. For example, Waller's
original lists contained the words 歯磨, 逆上る, and 火燵. These
spellings are all very rare. I have replaced these spellings with
their more common forms: 歯磨き, 遡る, and 炬燵.

## Install

Download **jlpt.zip** from the
[latest release](https://github.com/stephenmk/yomitan-jlpt-vocab/releases/latest)
and import it into Yomitan just like any other dictionary.

## Limitations

The lists used in this project were compiled by Jonathan Waller over
10 years ago, and I have made no attempt to curate them further.
Official vocabulary lists do not exist for the JLPT, so these lists
are essentially an educated guess. I can personally attest that more
than one word from Waller's N1 list appeared in vocabulary section of
the N2 exam in December 2021.
