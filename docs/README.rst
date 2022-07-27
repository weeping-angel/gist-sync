===============
Repo Gist Sync
===============

.. image:: https://img.shields.io/pypi/v/repo-gist-sync?label=PyPI
        :target: https://pypi.python.org/pypi/repo-gist-sync
        :alt: PYPI Package Version

.. image:: https://img.shields.io/pypi/dm/repo-gist-sync?color=darkgreen&label=Downloads
        :target: https://pypistats.org/packages/repo-gist-sync
        :alt: PYPI Monthly Download Stats

|

A library to synchronize git repository to Github Gists

.. mermaid::

    graph TD;

    A(local machine)
    A -->|push| B(Github repository)
    B -->|Github Actions| C(Gists)
    B -->|Github Actions| E(Gists)
    B -->|Github Actions| F(Gists)
    C --> D(Embeds)
    E --> G(Embeds)
    F --> H(Embeds)
    C --> I(Embeds)
    E --> J(Embeds)
    F --> K(Embeds)

Installation
------------

Install from `PyPI <https://pypi.org/project/repo-gist-sync/>`_

.. code-block:: console

        $ pip install repo-gist-sync

Dependencies: `requests`, `click`

Example
-------

.. code-block:: console

        gistdirsync --auth-token $GIST_TOKEN --directory /path/to/folder


How to use this in your CI/CD Pipeline
---------------------------------------


Features
--------

