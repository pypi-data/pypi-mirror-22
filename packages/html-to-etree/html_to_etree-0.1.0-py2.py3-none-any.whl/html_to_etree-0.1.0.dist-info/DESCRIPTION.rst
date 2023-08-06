=============
html to etree
=============

.. image:: https://img.shields.io/pypi/v/html-to-etree.svg
        :target: https://pypi.python.org/pypi/html-to-etree

.. image:: https://img.shields.io/pypi/pyversions/html-to-etree.svg
        :target: https://pypi.python.org/pypi/html-to-etree

.. image:: https://img.shields.io/travis/codinguncut/html-to-etree.svg
        :target: https://travis-ci.org/codinguncut/html-to-etree

.. image:: https://codecov.io/github/codinguncut/html-to-etree/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/codinguncut/html-to-etree

.. image:: https://requires.io/github/codinguncut/html-to-etree/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/codinguncut/html-to-etree/requirements/?branch=master

parse html to etree

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

=======
History
=======


0.1.0-dev (unreleased)
----------------------

* First release on PyPI.

