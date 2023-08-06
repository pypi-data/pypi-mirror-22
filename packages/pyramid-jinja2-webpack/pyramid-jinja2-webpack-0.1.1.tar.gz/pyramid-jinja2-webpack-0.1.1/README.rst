========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/pyramid-jinja2-webpack/badge?version=latest
    :target: http://pyramid-jinja2-webpack.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/JDeuce/python-pyramid-jinja2-webpack.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/JDeuce/python-pyramid-jinja2-webpack

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/JDeuce/python-pyramid-jinja2-webpack?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/JDeuce/python-pyramid-jinja2-webpack

.. |requires| image:: https://requires.io/github/JDeuce/python-pyramid-jinja2-webpack/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/JDeuce/python-pyramid-jinja2-webpack/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/JDeuce/python-pyramid-jinja2-webpack/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/github/JDeuce/python-pyramid-jinja2-webpack

.. |codecov| image:: https://codecov.io/github/JDeuce/python-pyramid-jinja2-webpack/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/JDeuce/python-pyramid-jinja2-webpack

.. |version| image:: https://img.shields.io/pypi/v/pyramid-jinja2-webpack.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/pyramid-jinja2-webpack

.. |commits-since| image:: https://img.shields.io/github/commits-since/JDeuce/python-pyramid-jinja2-webpack/v0.1.1.svg
    :alt: Commits since latest release
    :target: https://github.com/JDeuce/python-pyramid-jinja2-webpack/compare/v0.1.1...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/pyramid-jinja2-webpack.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/pyramid-jinja2-webpack

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pyramid-jinja2-webpack.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/pyramid-jinja2-webpack

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pyramid-jinja2-webpack.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/pyramid-jinja2-webpack


.. end-badges

Pyramid integration of jinja2_webpack

* Free software: BSD license

Installation
============

::

    pip install pyramid-jinja2-webpack

Documentation
=============

https://pyramid-jinja2-webpack.readthedocs.io/

Development
===========

To run the all tests run::

    tox


To run on a specific version of python run e.g.::

    tox -e py34
    tox -e py27

