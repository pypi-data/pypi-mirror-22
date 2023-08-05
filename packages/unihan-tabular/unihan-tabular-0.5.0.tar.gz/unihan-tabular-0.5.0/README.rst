*unihan-tabular* - tool to build `UNIHAN`_ into tabular-friendly formats
like python, JSON, CSV and YAML. Part of the `cihai`_ project.

|pypi| |docs| |build-status| |coverage| |license|

Unihan's data is disperved across multiple files in the format of::

    U+3400	kCantonese	jau1
    U+3400	kDefinition	(same as U+4E18 丘) hillock or mound
    U+3400	kMandarin	qiū
    U+3401	kCantonese	tim2
    U+3401	kDefinition	to lick; to taste, a mat, bamboo bark
    U+3401	kHanyuPinyin	10019.020:tiàn
    U+3401	kMandarin	tiàn

``unihan_tabular/process.py`` will download Unihan.zip and build all files into a
single tabular friendly format.

CSV (default output: ``./data/unihan.csv``)::

    char,ucn,kCantonese,kDefinition,kHanyuPinyin,kMandarin
    丘,U+3400,jau1,(same as U+4E18 丘) hillock or mound,,qiū
    㐁,U+3401,tim2,"to lock; to taste, a mat, bamboo bark",10019.020:"tiàn,tiàn"

``process.py`` supports command line arguments. See `unihan_tabular/process.py CLI
arguments`_ for information on how you can specify custom columns, files,
download URL's and output destinations.

Being built against unit tests. See the `Travis Builds`_ and
`Revision History`_.

.. _cihai: https://cihai.git-pull.com
.. _cihai-handbook: https://github.com/cihai/cihai-handbook
.. _cihai team: https://github.com/cihai?tab=members
.. _cihai-python: https://github.com/cihai/cihai-python
.. _unihan-tabular on github: https://github.com/cihai/unihan-tabular

Usage
-----

To download and build your own ``unihan.csv``:

.. code-block:: bash

   $ pip install unihan-tabular

.. code-block:: bash

    $ unihan-tabular

Creates ``data/unihan.csv``.

See `unihan_tabular/process.py CLI arguments`_ for advanced usage examples.

.. _unihan_tabular/process.py CLI arguments: http://unihan-tabular.readthedocs.org/en/latest/cli.html

Structure
---------

.. code-block:: bash

    # (future) when this package is stable, unihan.csv will be provided
    data/unihan.csv

    # stores downloaded Unihan.zip and it's txt file contents (.gitignore'd)
    data/build_files/

    # script to download + build a SDF csv of unihan.
    unihan_tabular/process.py

    # unit tests to verify behavior / consistency of builder
    tests/*

    # python 2/3 compatibility modules
    unihan_tabular/_compat.py
    unihan_tabular/unicodecsv.py

    # python module, public-facing python API.
    __init__.py
    unihan_tabular/__init__.py

    # utility / helper functions
    unihan_tabular/util.py


- ``data/unihan.csv`` - CSV export file.
- ``unihan_tabular/process.py`` - create a ``data/unihan.csv``.

When this module is stable, ``data/unihan.csv`` will have prepared
releases, without requires using ``unihan_tabular/process.py``. ``process.py``
will not require external libraries.

.. _MIT: http://opensource.org/licenses/MIT
.. _API: http://cihai.readthedocs.org/en/latest/api.html
.. _UNIHAN: http://www.unicode.org/charts/unihan.html

.. |pypi| image:: https://img.shields.io/pypi/v/unihan-tabular.svg
    :alt: Python Package
    :target: http://badge.fury.io/py/unihan-tabular

.. |build-status| image:: https://img.shields.io/travis/cihai/unihan-tabular.svg
   :alt: Build Status
   :target: https://travis-ci.org/cihai/unihan-tabular

.. |coverage| image:: https://codecov.io/gh/cihai/unihan-tabular/branch/master/graph/badge.svg
    :alt: Code Coverage
    :target: https://codecov.io/gh/cihai/unihan-tabular

.. |license| image:: https://img.shields.io/github/license/cihai/unihan-tabular.svg
    :alt: License 

.. |docs| image:: https://readthedocs.org/projects/unihan-tabular/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://readthedocs.org/projects/unihan-tabular/
