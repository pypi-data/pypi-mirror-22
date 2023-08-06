.. contents::

Introduction
============

Base content classes for document management system.

Features
--------

- Add dmsdocument type
- Add dmsmainfile type
- Add dmsfile type

Migration
---------

* From 1.0 version, collective.z3cform.rolefield has been replaced by dexterity.localrolesfield.
    After the upgrade step, you have to manually define dexterity localroles field configuration.
    See `dexterity.localrolesfield page information <https://pypi.python.org/pypi/dexterity.localrolesfield>`_


Tests
=====

This add-on is tested using Travis CI. The current status of the add-on is :

.. image:: https://secure.travis-ci.org/collective/collective.dms.basecontent.png
    :target: http://travis-ci.org/collective/collective.dms.basecontent
