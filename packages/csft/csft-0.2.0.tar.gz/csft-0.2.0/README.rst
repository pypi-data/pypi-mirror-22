csft - Count Sizes of File Types
================================

.. image:: https://travis-ci.org/yanqd0/csft.svg?branch=master
    :target: https://travis-ci.org/yanqd0/csft
.. image:: https://codecov.io/gh/yanqd0/csft/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/yanqd0/csft

A CLI to count sizes of file types in a directory, implemented by Python.

Install
--------

::

    pip install git+https://github.com/yanqd0/csft.git

Usage
-----

::

    csft PATH/TO/YOUR/PROJECT

Result
------

Something like this::

           type   size
    0            32859
    1   .sample  15321
    2      .xml  12349
    3      .pyc   7100
    4       .py   4221
    5      .yml   1085
    6      .rst    638
    7      .iml    455
    8        .2     41
    9        .1     41
    10       .0     41

Licence
-------

.. image:: https://img.shields.io/github/license/yanqd0/csft.svg
   :target: https://github.com/yanqd0/csft/blob/master/LICENSE
