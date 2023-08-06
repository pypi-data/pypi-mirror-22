=============
html to etree
=============

.. image:: https://img.shields.io/pypi/v/html-to-etree.svg
        :target: https://pypi.python.org/pypi/html-to-etree

.. image:: https://img.shields.io/pypi/pyversions/html-to-etree.svg
        :target: https://pypi.python.org/pypi/html-to-etree

.. image:: https://img.shields.io/travis/fluquid/html-to-etree.svg
        :target: https://travis-ci.org/fluquid/html-to-etree

.. image:: https://codecov.io/github/fluquid/html-to-etree/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/fluquid/html-to-etree

.. image:: https://requires.io/github/fluquid/html-to-etree/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/fluquid/html-to-etree/requirements/?branch=master

parse html to lxml etree

convenience methods for parsing html documents to lxml etree.
lxml has limited capabilities for handling different encodings, and this
library is intended as a reusable utility parsing byte-code html responses
into ElementTrees using sane character decoding.

* Free software: BSD license
* Python versions: 2.7, 3.4+

Features
--------

* parse html to lxml etree
* handle character decoding

Quickstart
----------

* `tree = parse_html_bytes(body=body_bytes, content_type='text/html')`
* `tree = parse_html_unicode(uni_string=body_unicode)`

Credits
-------

This package was created with Cookiecutter_ and the `codinguncut/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
