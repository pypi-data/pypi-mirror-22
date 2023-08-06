Deasy Package
=============

**Deasy** package provide a single cli command ***oo*** to intercat with odoo instances

**Deasy** is a Python package providing an easy way to
pilot and interact with **Odoo** instances through `CLI`.

Features supported:
    - manage informations of the Odoo instances,
    - backup and restore databases,
    - security audit,
    - search the xml-ids of records,
    - show data,
    - execute functions,
    - python shell,
    - JSON-RPC protocol (SSL supported),

Many thanks to OdooRPC_ and Odoo_.

Installation :
==============

.. code-block:: shell

    pip install deasy

Manage informations of Odoo instances :
=======================================

**Create an entry for an Odoo instance :**

.. code-block:: python

    oo create_section YOUR_SECTION_NAME


**List sections :**


.. code-block:: python

    oo sections


*You can also use  other commands to manage the informations of instances like `section_update` `delete_section` see `oo --help`*


Manage databases
================

**Backup a database :**

.. code-block:: python

    oo -l YOUR_SECTION_NAME backupdb /to/your/path


**Restore a database :**

.. code-block:: python

    oo -l YOUR_SECTION_NAME restoredb /from/your/path/yourdb.zip


*You can also use other commands to manage databses like `listdb` `dropdb` see `oo --help`*

Manage modules
==============

**Install some modules :**

.. code-block:: python

    oo -l YOUR_SECTION_NAME install sale,fleet,purchase

**Update some modules :**

.. code-block:: python

    oo -l YOUR_SECTION_NAME update sale,fleet,purchase


You can also uninstall modules using the argument `uninstall` see `oo --help`

Intercat with data
==================

*Show some data on res.partner :*

.. code-block:: python

    oo -l YOUR_SECTION_NAME data res.partner

With more options :

.. code-block:: python

    oo -l YOUR_SECTION_NAME data res.partner -f name -f customer -f supplier -d name like ASUSTEK -o name -l 1

See `oo data --help`

*Show fields of the model res.partner :*

.. code-block:: python

    oo -l YOUR_SECTION_NAME fields res.partner

Launch python shell
===================

*Show some data on res.partner :*

.. code-block:: python

    oo -l YOUR_SECTION_NAME shell
    >>> Partner = odoo.env['res.partner']
    >>> partner_ids = Partner.search([])
    >>> for partner in Partner.browse(partner_ids):
    ...     print partner.name
    ...

Refer to OdooRPC_ documentation

You can also retrieve data with a simple command :

.. code-block:: python

    oo -l YOUR_SECTION_NAME shell
    >>> partners = browse('res.partner') # or browse('res.partner', [])
    >>> for partner in partners :
    ...     print partner.name
    ...


Licence
=======

This software is made available under the LGPL v3 license.

Bug Tracker
===========

Please, feel free to report bugs or suggestions in the `Bug Tracker <https://github.com/chermed/deasy/issues>`_!

Credits:
========

Mohamed Cherkaoui <http://mohamedcherkaoui.com>


.. _OdooRPC: https://pypi.python.org/pypi/OdooRPC/

.. _Odoo: https://www.odoo.com



News
====

2.0.0
-----

*Release date: 03-Jun-2017*

* First stable version

