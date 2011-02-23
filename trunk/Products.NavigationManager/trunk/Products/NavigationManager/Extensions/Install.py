# File: Install.py
#
# Copyright (c) 2006 by []
# Generator: ArchGenXML Version 1.4.1
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

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'


import os.path
import sys
from StringIO import StringIO
from sets import Set
from App.Common import package_home
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import manage_addTool
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from zExceptions import NotFound, BadRequest

from Products.Archetypes.Extensions.utils import installTypes
from Products.Archetypes.Extensions.utils import install_subskin
from Products.Archetypes.config import TOOL_NAME as ARCHETYPETOOLNAME
from Products.Archetypes.atapi import listTypes
from Products.NavigationManager.config import PROJECTNAME
from Products.NavigationManager.config import product_globals as GLOBALS

try:
    from ZODB.Transaction import get_transaction
except ImportError:
    from transaction import get as get_transaction

def install(self):
    """ External Method to install NavigationManager """
    out = StringIO()
    print >> out, "Installation log of %s:" % PROJECTNAME

    # If the config contains a list of dependencies, try to install
    # them.  Add a list called DEPENDENCIES to your custom
    # AppConfig.py (imported by config.py) to use it.
    try:
        from Products.NavigationManager.config import DEPENDENCIES
    except:
        DEPENDENCIES = []
    portal = getToolByName(self,'portal_url').getPortalObject()
    quickinstaller = portal.portal_quickinstaller
    for dependency in DEPENDENCIES:
        print >> out, "Installing dependency %s:" % dependency
        quickinstaller.installProduct(dependency)
        get_transaction().commit(1)

    classes = listTypes(PROJECTNAME)
    installTypes(self, out,
                 classes,
                 PROJECTNAME)
    install_subskin(self, out, GLOBALS)



    #autoinstall tools
    portal = getToolByName(self,'portal_url').getPortalObject()
    for t in ['NavigationManager']:
        try:
            portal.manage_addProduct[PROJECTNAME].manage_addTool(t)
        except BadRequest:
            # if an instance with the same name already exists this error will
            # be swallowed. Zope raises in an unelegant manner a 'Bad Request' error
            pass
        except:
            e = sys.exc_info()
            if e[0] != 'Bad Request':
                raise
    #hide tools in the navigation
    portalProperties = getToolByName(self, 'portal_properties', None)
    if portalProperties is not None:
        navtreeProperties = getattr(portalProperties, 'navtree_properties', None)
        if navtreeProperties:
            navtreeProperties.idsNotToList = list(navtreeProperties.idsNotToList) + \
                                  [toolname for toolname in ['portal_navigationmanager'] \
                                            if toolname not in navtreeProperties.idsNotToList]

    # try to call a workflow install method
    # in 'InstallWorkflows.py' method 'installWorkflows'
    try:
        installWorkflows = ExternalMethod('temp',
                                          'temp',
                                          PROJECTNAME+'.InstallWorkflows',
                                          'installWorkflows').__of__(self)
    except NotFound:
        installWorkflows = None

    if installWorkflows:
        print >> out, 'Workflow Install:'
        res = installWorkflows(self, out)
        print >> out, res or 'no output'
    else:
        print >> out, 'no workflow install'


    # enable portal_factory for given types
    factory_tool = getToolByName(self, 'portal_factory')
    factory_types = [
        ] + factory_tool.getFactoryTypes().keys()
    factory_tool.manage_setPortalFactoryTypes(listOfTypeIds=factory_types)

    from Products.NavigationManager.config import STYLESHEETS
    try:
        portal_css = getToolByName(portal, 'portal_css')
        for stylesheet in STYLESHEETS:
            try:
                portal_css.unregisterResource(stylesheet['id'])
            except:
                pass
            defaults = {'id': '',
            'media': 'all',
            'enabled': True}
            defaults.update(stylesheet)
            portal_css.manage_addStylesheet(**defaults)
    except:
        # No portal_css registry
        pass
    from Products.NavigationManager.config import JAVASCRIPTS
    try:
        portal_javascripts = getToolByName(portal, 'portal_javascripts')
        for javascript in JAVASCRIPTS:
            try:
                portal_javascripts.unregisterResource(javascript['id'])
            except:
                pass
            defaults = {'id': ''}
            defaults.update(javascript)
            portal_javascripts.registerScript(**defaults)
    except:
        # No portal_javascripts registry
        pass

    # try to call a custom install method
    # in 'AppInstall.py' method 'install'
    try:
        install = ExternalMethod('temp', 'temp',
                                 PROJECTNAME + '.AppInstall', 'install')
    except NotFound:
        install = None

    if install:
        print >> out, 'Custom Install:'
        res = install(self)
        if res:
            print >> out, res
        else:
            print >> out, 'no output'
    else:
        print >> out, 'no custom install'


    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.setImportContext('profile-NavigationManager:navigationmanager')
    setup_tool.runAllImportSteps()
        
    return out.getvalue()

def uninstall(self):
    out = StringIO()

    # unhide tools
    portalProperties = getToolByName(self, 'portal_properties', None)
    if portalProperties is not None:
        navtreeProperties = getattr(portalProperties, 'navtree_properties', None)
        if navtreeProperties:
            navtreeProperties.idsNotToList = list(navtreeProperties.idsNotToList)
            for toolname in [toolname for toolname in ['portal_navigationmanager'] \
                            if toolname not in navtreeProperties.idsNotToList]:
                if toolname in navtreeProperties.idsNotToList:
                    navtreeProperties.idsNotToList.remove(toolname)

    # try to call a workflow uninstall method
    # in 'InstallWorkflows.py' method 'uninstallWorkflows'
    try:
        uninstallWorkflows = ExternalMethod('temp', 'temp',
                                            PROJECTNAME + '.InstallWorkflows',
                                            'uninstallWorkflows').__of__(self)
    except NotFound:
        uninstallWorkflows = None

    if uninstallWorkflows:
        print >> out, 'Workflow Uninstall:'
        res = uninstallWorkflows(self, out)
        print >> out, res or 'no output'
    else:
        print >> out, 'no workflow uninstall'

    # try to call a custom uninstall method
    # in 'AppInstall.py' method 'uninstall'
    try:
        uninstall = ExternalMethod('temp', 'temp',
                                   PROJECTNAME + '.AppInstall', 'uninstall')
    except:
        uninstall = None

    if uninstall:
        print >> out, 'Custom Uninstall:'
        res = uninstall(self)
        if res:
            print >> out, res
        else:
            print >> out, 'no output'
    else:
        print >> out, 'no custom uninstall'

    return out.getvalue()
