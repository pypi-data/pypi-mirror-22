The VIS Framework
=================

The VIS Framework for Music Analysis

[![Build Status](https://travis-ci.org/ELVIS-Project/vis-framework.svg?branch=master)](https://travis-ci.org/ELVIS-Project/vis-framework)
[![Coverage Status](https://coveralls.io/repos/ELVIS-Project/vis-framework/badge.svg?branch=master&service=github)](https://coveralls.io/github/ELVIS-Project/vis-framework?branch=master)
[![Latest Version](https://img.shields.io/pypi/v/vis-framework.svg)](https://pypi.python.org/pypi/vis-framework/)
[![License](https://img.shields.io/badge/license-AGPL%203.0-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.html)

The VIS Framework is a Python package that uses the music21 and pandas libraries to build a flexible system for writing computational music analysis programs.

Copyright Information:
* All source code is subject to the GNU AGPL 3.0 Licence. A copy of this licence is included as doc/apg-3.0.txt.
* All other content is subject to the CC-BY-SA Unported 3.0 Licence. A copy of this licence is included as doc/CC-BY-SA.txt
* All content in the test_corpus directory is subject to the licence in the file test_corpus/test_corpus_licence.txt

Software Dependencies
=====================

The VIS Framework uses many software libraries to help with analysis. These are required dependencies:

- [Python 3.5](https://www.python.org)
- [music21](http://web.mit.edu/music21/)
- [pandas](http://pandas.pydata.org)
- [multi_key_dict](https://pypi.python.org/pypi/multi_key_dict)
- [requests](https://pypi.python.org/pypi/requests/)

These are recommended dependencies:

- [numexpr](https://pypi.python.org/pypi/numexpr) (improved performance for pandas)
- [Bottleneck](https://pypi.python.org/pypi/Bottleneck) (improved performance for pandas)
- [tables](https://pypi.python.org/pypi/tables) (HDF5 output for pandas)
- [openpyxl](https://pypi.python.org/pypi/openpyxl) (Excel output for pandas)
- [mock](https://pypi.python.org/pypi/mock) (for testing)
- [coverage](https://pypi.python.org/pypi/coverage) (for testing)
- [python-coveralls](https://pypi.python.org/pypi/python-coveralls) (to for automated coverage with coveralls.io)
- [matplotlib](https://pypi.python.org/pypi/matplotlib) (plotting)
- [scipy](https://pypi.python.org/pypi/scipy) (plotting)

Documentation
=============

You can find documentation here:
- [Major Release Documentation](http://vis-framework.readthedocs.org/)
- [Stable Release Documentation](http://vis-framework.readthedocs.org/en/stable/)
- [Latest Release Documentation](http://vis-framework.readthedocs.org/en/latest/), a.k.a. "bleeding edge" 

Citation
========

If you wish to cite the VIS Framework, please use this ISMIR 2014 article:

Antila, Christopher and Julie Cumming. "The VIS Framework: Analyzing Counterpoint in Large Datasets."
    In Proceedings of the International Society for Music Information Retrieval, 2014.

A BibTeX entry for LaTeX users is

```
@inproceedings{,
    title = {The VIS Framework: Analyzing Counterpoint in Large Datasets},
    author = {Antila, Christopher and Cumming, Julie},
    booktitle = {Proceedings of the International Society for Music Information Retrieval},
    location = {Taipei, Taiwan},
    year = {2014},
}
```

You may also wish to cite the software itself:

Antila, Christopher and Jamie Klassen. The VIS Framework for Music Analysis. Montréal: The ELVIS Project, 2014. URL https://github.com/ELVIS-Project/vis.

A BibTeX entry for LaTeX users is

```
@Manual{,
    title = {The VIS Framework for Music Analysis},
    author = {Antila, Christopher and Klassen, Jamie},
    organization = {The ELVIS Project},
    location = {Montréal, Québec},
    year = {2014},
    url = {https://github.com/ELVIS-Project/vis},
}
```
