===============
Django Material
===============

Material design for Django Forms and Admin. Template driven.

.. image:: https://img.shields.io/pypi/v/django-material.svg
    :target: https://pypi.python.org/pypi/django-material
.. image:: https://img.shields.io/pypi/wheel/django-material.svg
    :target: https://pypi.python.org/pypi/django-material
.. image:: https://img.shields.io/pypi/status/django-material.svg
    :target: https://pypi.python.org/pypi/django-material
.. image:: https://travis-ci.org/viewflow/django-material.svg
    :target: https://travis-ci.org/viewflow/django-material
.. image:: https://img.shields.io/pypi/pyversions/django-material.svg
    :target: https://pypi.python.org/pypi/django-material
.. image:: https://img.shields.io/pypi/l/Django.svg
    :target: https://raw.githubusercontent.com/viewflow/django-material/master/LICENSE.txt
.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/viewflow/django-material
   :target: https://gitter.im/viewflow/django-material?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

Django-Material works with Django 1.8/1.9/1.10/1.11

Django-Material 1.x branch going to be supported till Django 1.8 lifetime (April 2018)

Tested with:

.. image:: demo/static/img/browserstack_small.png
  :target:  http://browserstack.com/

Overview
========

- Forms - New way to render django forms

  * Strong python/html code separation
  * Easy redefinition of particular fields rendering
  * Complex form layout support

- Frontend - Quick starter template for modular applications development

- Admin - Material-designed django admin

Demo: http://forms.viewflow.io/

.. image:: .screen.png
   :width: 400px

           Documentation
=============

http://docs.viewflow.io/material_forms.html

License
=======

Django Material is an Open Source project licensed under the terms of the `BSD3 license <https://github.com/viewflow/django-material/blob/master/LICENSE.txt>`_

Django Material Pro has a commercial-friendly license and distributed as part of Viewflow Pro


Changelog
=========

1.0.0 2017-29-30 - Stable
-------------------------

- Django 1.11 support
- Update MaterializeCSS to 0.98.2
- Fix missing badges in shipped MaterializeCSS build
- Localization added: German/French/Spainish/Korean/Chinese
- Forms - Fix allows to use html in a `help_text` of widgets
- Frontend - Improved Login/Logout/403/404/500 service screen templates
- Admin - fix application list layout
