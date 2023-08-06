Django Arctic
=============

|PyPi version| |Build Status| |Coverage Status| |Read the Docs|

Django Arctic is a framework that simplifies the creation of custom
content management systems. It provides a default responsive user
interface, extends several of the Django Generic Views with extra
features and adds role based authentication.

.. figure:: docs/img/arctic_screenshot.png
   :alt: arctic screenshot

   arctic screenshot

Why
---

There are a lot of content management systems in the market that are a
good fit for the implementation of many web sites. Most CMS systems make
assumptions about the data model for posts, authentication and the
administration interface.

There is however a tipping point, where the need to customize a CMS
product is extensive enough that it ends up creating a more complex
implementation than if the product was developed directly with a generic
framework. This is specially true when the core of a CMS needs to be
changed.

This is the case that Arctic wants to solve, creation of a CMS with a
high degree of customization. Instead of being a ready-to-use CMS,
Arctic is a framework that facilitates the construction of content
management systems.

Compatibility
-------------

-  Python 2.7, 3.5, 3.6
-  Django 1.8, 1.9, 1.10

Features
--------

-  Configurable menu
-  Default responsive UI
-  Role based authentication with permissions that can be object based.
-  Optional tabbed interface to visually link multiple Views.
-  ListViews support nested fields, sorting, filtering and linking.
-  Forms with default improved widgets for datetime and option fields.

.. |PyPi version| image:: https://img.shields.io/pypi/v/django-arctic.svg
   :target: https://pypi.python.org/pypi/django-arctic/
.. |Build Status| image:: https://travis-ci.org/sanoma/django-arctic.svg?branch=develop
   :target: https://travis-ci.org/sanoma/django-arctic
.. |Coverage Status| image:: https://coveralls.io/repos/github/sanoma/django-arctic/badge.svg?branch=develop
   :target: https://coveralls.io/github/sanoma/django-arctic
.. |Read the Docs| image:: https://readthedocs.org/projects/django-arctic/badge/?version=latest
   :target: https://django-arctic.readthedocs.io/en/latest/


