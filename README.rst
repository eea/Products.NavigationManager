======================
EEA Navigation Manager
======================
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/Products.NavigationManager/develop
  :target: https://ci.eionet.europa.eu/job/eea/job/Products.NavigationManager/job/develop/display/redirect
  :alt: Develop
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/Products.NavigationManager/master
  :target: https://ci.eionet.europa.eu/job/eea/job/Products.NavigationManager/job/master/display/redirect
  :alt: Master

This is a package that generates the portlet navigation for EEA Site

Contents
========

.. contents::

Getting started
===============

To generate a navigation portlet, the code does:

* portlet template: navigation.pt
* looks for adapters for INavigationSections for current context. In this
  way other sections can be defined by the context
* with the list of sections, it calls python:view.createNavSection(section.value, section.title)
* to render the section it uses the section.pt template
* here it calls view.createNavTree(section=section)


Source code
===========

- Latest source code (Plone 4 compatible):
  https://github.com/eea/Products.NavigationManager


Copyright and license
=====================
The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

The EEA Navigation Manager (the Original Code) is free software;
you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later
version.

More details under docs/License.txt


Funding
=======

EEA_ - European Environment Agency (EU)

.. _EEA: https://www.eea.europa.eu/
