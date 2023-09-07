# Taxi1500-c v1.0

## Download
Version 1.0 of the Taxi1500 corpora can be downloaded via [this link](https://cis.lmu.de/~yehao/data/Taxi1500-c_v1.0.zip).

## Description
We used the following process to obtain Bible editions that are either open access or have permissive licenses.

### Metadata keyword matching
All PBC editions have a metadata section at the start of the file which contains license information, translator, and release year, etc.

We search for phrases indicating a permissive license status. If an edition’s metadata indicates a permissive license, we treat it as distributable.

### Metadata year matching
For simplicity, we treat any edition published at least 100 years ago, i.e. before 1923, as distributable.

We match the “year_short” field in the metadata for the release year.

### Pre-compiled lists of distributable editions
[PNG Scriptures](https://png.bible/) has a list of editions for Papua New Guinean languages, which are all freely distributable.

[ebible.org](https://ebible.org/Scriptures/copyright.php) lists many public domain and open access editions.

All PNG editions are distributable. We compile a list of PNG editions under 1000Langs (those that end with “.png.txt”).

We extract isos in the public domain and open access lists from ebible.org and isos from PNG. If one of the isos has only one edition under 1000Langs, we manually check if the edition corresponds to the open edition.

### Translation ID matching
Every Bible edition from ebible.org has a translation ID associated with it, which is usually six-character long and consists of two parts: the language’s iso and a letter combination which refer to a specific translation. For example ENGASV refers to “English, American Standard Version”.

We extract the list of translation IDs that belong to public domain and open access editions.

We match the translation IDs against the editions under 1000Langs, if the filename contains one of the translation IDs, we treat it as distributable.

