kinto-wizard
============

|pypi| |ci| |coverage|

.. |pypi| image:: https://img.shields.io/pypi/v/kinto-wizard.svg
    :target: https://pypi.python.org/pypi/kinto-wizard
.. |ci| image:: https://travis-ci.org/Kinto/kinto-wizard.svg?branch=master
    :target: https://travis-ci.org/Kinto/kinto-wizard
.. |coverage| image:: https://coveralls.io/repos/github/Kinto/kinto-wizard/badge.svg?branch=master
    :target: https://coveralls.io/github/Kinto/kinto-wizard?branch=master

kinto-wizard is a tool that lets you setup an entire Kinto server from
a Yaml file, or inspect an existing server and output a Yaml file.

You can define Kinto objects (bucket, collection, groups, records)
and configure their attributes and permissions.

`Read more information about the file structure <https://github.com/Kinto/kinto/wiki/Handling-permission-on-a-Kinto-Server>`_


Installation
------------

The last release
~~~~~~~~~~~~~~~~

.. code-block:: bash

    pip install kinto-wizard


The development version
~~~~~~~~~~~~~~~~~~~~~~~

After having cloned the repo:

.. code-block:: bash

    pip install -e .


How to use it?
--------------

Load
~~~~

.. code-block:: bash

    kinto-wizard load \
        --server https://kinto-writer.stage.mozaws.net/v1 \
        --auth admin:credentials \
        new-config.yml

Dump
~~~~

.. code-block:: bash

    kinto-wizard dump \
        --server https://kinto-writer.stage.mozaws.net/v1 \
        --auth admin:credentials \
        > current-config.yml

The dump also accepts a ``--full`` option that will output object data and collection
records.


Changelog
=========

This document describes changes between each past release.

2.0.0 (2017-05-22)
------------------

**Breaking changes**

- Upgrade to kinto-http 8.0.0 with Python 3.5+ support.
- The ``--full`` option of the ``dump`` command now outputs records (#16)

**New features**

- The ``load`` command now supports records (#16)


1.0.0 (2016-11-22)
------------------

**Initial version**

- Supports dumping/loading groups and permissions from/to a YAML file.


Contributors
============

* Rémy Hubscher <rhubscher@mozilla.com>
* Mathieu Leplatre <mathieu@mozilla.com>
* Gabriela Surita <gabsurita@gmail.com>


