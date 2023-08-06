.. image:: https://travis-ci.org/Jackevansevo/basic-utils.svg?branch=master
    :target: https://travis-ci.org/Jackevansevo/basic-utils

.. image:: https://coveralls.io/repos/github/Jackevansevo/basic-utils/badge.svg?branch=master
    :target: https://coveralls.io/github/Jackevansevo/basic-utils?branch=master

.. image:: https://img.shields.io/pypi/pyversions/basic-utils.svg
    :target: https://pypi.python.org/pypi/basic-utils

.. image:: https://readthedocs.org/projects/basic-utils/badge/?version=latest
    :target: http://basic-utils.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

============
Basic utils
============

Useful utilities for Python 3.4+


Documentation
=============

See what's available by reading the docs here_

.. _here: http://basic-utils.readthedocs.io/en/latest/?badge=latest

Installation
=============

Install through PyPi with the following::

    pip3 install basic-utils


FAQ
===

Q: Does anyone use this?

A: Not that I know of

Q: Should I use this?

A: Sure (but at your own risk)

Q: Why doesn't this have X?

A: Open an issue or submit a pull request


Similar Projects
================

- Toolz_
- UnderScoreJS_

.. _Toolz: https://github.com/pytoolz/toolz
.. _UnderScoreJS: https://github.com/jashkenas/underscore


Running Tests
=============

(Optional) Create a virtualenv:

.. code-block:: bash

    python3 -m venv venv

Activate the virtualenv

.. code-block:: bash

    venv/bin/activate

Install requirements

.. code-block:: bash

    pip install -e ."[test]"

Install requirements and run:

.. code-block:: bash

    pytest

To get test coverage:

.. code-block:: bash

    scripts/test
