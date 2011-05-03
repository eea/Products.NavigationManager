# -*- coding: utf-8 -*-
#
# File: EEAContentTypeTestCase.py
#
# Copyright (c) 2006 by []
# Generator: ArchGenXML Version 1.5.1-svn
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

#
# Base TestCase for NavigationManager
#

from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.GenericSetup import EXTENSION, profile_registry

PRODUCTS = ['FiveSite', 'NavigationManager']

profile_registry.registerProfile(
                    'testfixture',
                    'test:NavigationManager',
                    'Extension profile for testing NavigationManager',
                    'profile/testfixture',
                    'NavigationManager',
                    EXTENSION,
                    for_=IPloneSiteRoot)

@onsetup
def setup_navigationmanager():
    fiveconfigure.debug_mode = True
    import Products.Five
    import Products.FiveSite
    import eea.plone3compat
    zcml.load_config('meta.zcml', Products.Five)
    zcml.load_config('configure.zcml', Products.FiveSite)
    zcml.load_config('configure.zcml', eea.plone3compat)
    zcml.load_config('configure.zcml', Products.NavigationManager)
    fiveconfigure.debug_mode = False

    PloneTestCase.installProduct('Five')
    PloneTestCase.installProduct('FiveSite')
    PloneTestCase.installProduct('NavigationManager')

setup_navigationmanager()
PloneTestCase.setupPloneSite(extension_profiles = ['NavigationManager:testfixture'], products = PRODUCTS)

class NavigationManagerTestCase(PloneTestCase.PloneTestCase):
    """Base TestCase for NavigationManager."""

class NavigationManagerFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    """ """
