*cihaidata-unihan* - tool to build `unihan`_ into `simple data format`
CSV format. Part of the `cihai`_ project.

|pypi| |docs| |build-status| |coverage| |license|

Unihan's data is disperved across multiple files in the format of::

    U+3400	kCantonese	jau1
    U+3400	kDefinition	(same as U+4E18 丘) hillock or mound
    U+3400	kMandarin	qiū
    U+3401	kCantonese	tim2
    U+3401	kDefinition	to lick; to taste, a mat, bamboo bark
    U+3401	kHanyuPinyin	10019.020:tiàn
    U+3401	kMandarin	tiàn

``script/process.py`` will download Unihan.zip and build all files into a
single tabular CSV (default output: ``./data/unihan.csv``)::

    char,ucn,kCantonese,kDefinition,kHanyuPinyin,kMandarin
    丘,U+3400,jau1,(same as U+4E18 丘) hillock or mound,,qiū
    㐁,U+3401,tim2,"to lock; to taste, a mat, bamboo bark",10019.020:"tiàn,tiàn"

``process.py`` supports command line arguments. See `script/process.py CLI
arguments`_ for information on how you can specify custom columns, files,
download URL's and output destinations.

Being built against unit tests. See the `Travis Builds`_ and
`Revision History`_.

.. _cihai: https://cihai.git-pull.com
.. _cihai-handbook: https://github.com/cihai/cihai-handbook
.. _cihai team: https://github.com/cihai?tab=members
.. _cihai-python: https://github.com/cihai/cihai-python
.. _cihaidata-unihan on github: https://github.com/cihai/cihaidata-unihan

Usage
-----

To download and build your own ``unihan.csv``:

.. code-block:: bash

    $ ./scripts/process.py

Creates ``data/unihan.csv``.

See `script/process.py CLI arguments`_ for advanced usage examples.

.. _script/process.py CLI arguments: http://cihaidata-unihan.readthedocs.org/cli.html


Structure
---------

.. code-block:: bash

    # dataset metadata, schema information.
    datapackage.json

    # (future) when this package is stable, unihan.csv will be provided
    data/unihan.csv

    # stores downloaded Unihan.zip and it's txt file contents (.gitignore'd)
    data/build_files/

    # script to download + build a SDF csv of unihan.
    scripts/process.py

    # unit tests to verify behavior / consistency of builder
    tests/*

    # python 2/3 compatibility modules
    script/_compat.py
    script/unicodecsv.py

    # python module, public-facing python API.
    __init__.py
    scripts/__init__.py

    # utility / helper functions
    scripts/util.py


Cihai is *not* required for:

- ``data/unihan.csv`` - `simple data format`_ compatible csv file.
- ``scripts/process.py`` - create a ``data/unihan.csv``.

When this module is stable, ``data/unihan.csv`` will have prepared
releases, without requires using ``scripts/process.py``. ``process.py``
will not require external libraries.

Examples
--------

- https://github.com/datasets/gdp
- https://github.com/datasets/country-codes

Related links:

- CSV *Simple Data Format* (SDF): http://data.okfn.org/standards/simple-data-format
- Tools: http://data.okfn.org/tools


.. _Travis Builds: https://travis-ci.org/cihai/cihaidata-unihan/builds
.. _Revision History: https://github.com/cihai/cihaidata-unihan/commits/master
.. _cjklib: http://cjklib.org/0.3/
.. _current datasets: http://cihai.readthedocs.org/en/latest/api.html#datasets
.. _permissively licensing your dataset: http://cihai.readthedocs.org/en/latest/information_liberation.html

==============  ==========================================================
Python support  Python 2.7, >= 3.3, pypy/pypy3
Source          https://github.com/cihai/cihaidata-unihan
Docs            https://cihaidata-unihan.git-pull.com
Changelog       https://cihaidata-unihan.git-pull.com/en/latest/history.html
API             https://cihaidata-unihan.git-pull.com/en/latest/api.html
Issues          https://github.com/cihai/cihaidata-unihan/issues
Travis          https://travis-ci.org/cihai/cihaidata-unihan
Test coverage   https://codecov.io/gh/cihai/cihaidata-unihan
pypi            https://pypi.python.org/pypi/cihaidata-unihan
OpenHub         https://www.openhub.net/p/cihaidata-unihan
License         `MIT`_.
git repo        .. code-block:: bash

                    $ git clone https://github.com/cihai/cihaidata-unihan.git
install dev     .. code-block:: bash

                    $ git clone https://github.com/cihai/cihaidata-unihan.git cihai
                    $ cd ./cihai
                    $ virtualenv .env
                    $ source .env/bin/activate
                    $ pip install -e .
tests           .. code-block:: bash

                    $ python setup.py test
==============  ==========================================================

.. _MIT: http://opensource.org/licenses/MIT
.. _Documentation: http://cihai.readthedocs.org/en/latest/
.. _API: http://cihai.readthedocs.org/en/latest/api.html
.. _Unihan: http://www.unicode.org/charts/unihan.html
.. _datapackages: http://dataprotocols.org/data-packages/
.. _datapackage.json format: https://github.com/datasets/gdp/blob/master/datapackage.json
.. _json table schema: http://dataprotocols.org/json-table-schema/
.. _simple data format: http://data.okfn.org/standards/simple-data-format
.. _cihai dataset API: http://cihai.readthedocs.org/en/latest/extending.html
.. _PEP 301\: python package format: http://www.python.org/dev/peps/pep-0301/

.. |pypi| image:: https://img.shields.io/pypi/v/cihaidata-unihan.svg
    :alt: Python Package
    :target: http://badge.fury.io/py/cihaidata-unihan

.. |build-status| image:: https://img.shields.io/travis/cihai/cihaidata-unihan.svg
   :alt: Build Status
   :target: https://travis-ci.org/cihai/cihaidata-unihan

.. |coverage| image:: https://codecov.io/gh/cihai/cihaidata-unihan/branch/master/graph/badge.svg
    :alt: Code Coverage
    :target: https://codecov.io/gh/cihai/cihaidata-unihan

.. |license| image:: https://img.shields.io/github/license/cihai/cihaidata-unihan.svg
    :alt: License 

.. |docs| image:: https://readthedocs.org/projects/cihaidata-unihan/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://readthedocs.org/projects/cihaidata-unihan/
