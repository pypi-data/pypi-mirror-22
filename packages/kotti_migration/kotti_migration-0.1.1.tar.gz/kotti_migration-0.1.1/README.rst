kotti_migration
***************

This is an extension to Kotti that allows content types to be exported and imported to and from your site.

|pypi|_
|downloads_month|_
|license|_
|build_status_stable|_

.. |pypi| image:: https://img.shields.io/pypi/v/kotti_migration.svg?style=flat-square
.. _pypi: https://pypi.python.org/pypi/kotti_migration/

.. |downloads_month| image:: https://img.shields.io/pypi/dm/kotti_migration.svg?style=flat-square
.. _downloads_month: https://pypi.python.org/pypi/kotti_migration/

.. |license| image:: https://img.shields.io/pypi/l/kotti_migration.svg?style=flat-square
.. _license: http://www.repoze.org/LICENSE.txt

.. |build_status_stable| image:: https://img.shields.io/travis/b4oshany/kotti_migration/production.svg?style=flat-square
.. _build_status_stable: http://travis-ci.org/b4oshany/kotti_migration

`Find out more about Kotti`_

Development happens at https://github.com/b4oshany/kotti_migration

.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti

Setup
=====

To enable the extension in your Kotti site, activate the configurator::

    kotti.configurators =
        kotti_migration.kotti_configure

Ignore Specific Kotti Content Types
=====================================

The snippet below will ignore all PDF Content type found in your the exported json file when importing.
The snippet below should be placed in your ini file::

    migration.ignore_content_types =
        kotti_pdf.resources.PDF

Usage
======

Go to any content type on your site and append **@@import** to the url, for instance::


    http://localhost:8080/@@import


Development
===========

|build_status_master|_

.. |build_status_master| image:: https://img.shields.io/travis/b4oshany/kotti_migration/master.svg?style=flat-square
.. _build_status_master: http://travis-ci.org/b4oshany/kotti_migration

Contributions to kotti_migration are highly welcome.
Just clone its `Github repository`_ and submit your contributions as pull requests.

.. _alembic: http://pypi.python.org/pypi/alembic
.. _alembic documentation: http://alembic.readthedocs.org/en/latest/index.html
.. _tracker: https://github.com/b4oshany/kotti_migration/issues
.. _Github repository: https://github.com/b4oshany/kotti_migration
