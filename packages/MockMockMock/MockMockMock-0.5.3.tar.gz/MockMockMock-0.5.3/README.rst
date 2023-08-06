**DO NOT USE THIS LIBRARY**: there is now a standard `mocking library in Python <https://docs.python.org/3/library/unittest.mock.html>`__.
I will not fix anything in this library and I'm migrating my own projects to ``unittest.mock``.

MockMockMock is a Python (2.7+ and 3.3+) `mocking <http://en.wikipedia.org/wiki/Mock_object>`__ library
focusing on very explicit definition of the mocks' behaviour.
It allows as-specific-as-needed unit-tests as well as more generic ones.

It's licensed under the `MIT license <http://choosealicense.com/licenses/mit/>`__.
It's available on the `Python package index <http://pypi.python.org/pypi/MockMockMock>`__,
its `documentation is hosted by Python <http://pythonhosted.org/MockMockMock>`__
and its source code is on `GitHub <https://github.com/jacquev6/MockMockMock>`__.

.. image:: https://img.shields.io/travis/jacquev6/MockMockMock/master.svg
    :target: https://travis-ci.org/jacquev6/MockMockMock

.. image:: https://img.shields.io/coveralls/jacquev6/MockMockMock/master.svg
    :target: https://coveralls.io/r/jacquev6/MockMockMock

.. image:: https://img.shields.io/codeclimate/github/jacquev6/MockMockMock.svg
    :target: https://codeclimate.com/github/jacquev6/MockMockMock

.. image:: https://img.shields.io/scrutinizer/g/jacquev6/MockMockMock.svg
    :target: https://scrutinizer-ci.com/g/jacquev6/MockMockMock

.. image:: https://img.shields.io/pypi/dm/MockMockMock.svg
    :target: https://pypi.python.org/pypi/MockMockMock

.. image:: https://img.shields.io/pypi/l/MockMockMock.svg
    :target: https://pypi.python.org/pypi/MockMockMock

.. image:: https://img.shields.io/pypi/v/MockMockMock.svg
    :target: https://pypi.python.org/pypi/MockMockMock

.. image:: https://img.shields.io/pypi/pyversions/MockMockMock.svg
    :target: https://pypi.python.org/pypi/MockMockMock

.. image:: https://img.shields.io/pypi/status/MockMockMock.svg
    :target: https://pypi.python.org/pypi/MockMockMock

.. image:: https://img.shields.io/github/issues/jacquev6/MockMockMock.svg
    :target: https://github.com/jacquev6/MockMockMock/issues

.. image:: https://badge.waffle.io/jacquev6/MockMockMock.png?label=ready&title=ready
    :target: https://waffle.io/jacquev6/MockMockMock

.. image:: https://img.shields.io/github/forks/jacquev6/MockMockMock.svg
    :target: https://github.com/jacquev6/MockMockMock/network

.. image:: https://img.shields.io/github/stars/jacquev6/MockMockMock.svg
    :target: https://github.com/jacquev6/MockMockMock/stargazers

Quick start
===========

Install from PyPI::

    $ pip install MockMockMock

Import:

>>> from MockMockMock import *

Write some code to test:

>>> def f(source):
...   return source.get(42) * 2

Mock:

>>> mocks = Engine()
>>> mock = mocks.create("mocks")

Expect:

>>> mock.expect.get(42).and_return(12)

Test:

>>> assert f(mock.object) == 24

Verify all expected calls have been done:

>>> mocks.tearDown()
