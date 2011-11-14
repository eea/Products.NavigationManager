# -*- coding: utf-8 -*-
#
# File: testFrontpage.py
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

from Products.NavigationManager.tests.NavigationManagerTestCase import NavigationManagerTestCase
from zope.app.component.hooks import setSite
#from zope.app.event.objectevent import ObjectModifiedEvent
#from zope.event import notify

class TestCatalog(NavigationManagerTestCase):
    """ Test-cases for class(es) relations. """

    def afterSetUp(self):
        setSite(self.portal)
        self.setRoles('Manager')
        wf = self.workflow = self.portal.portal_workflow
        self.catalog = self.portal.portal_catalog

        self.folder.invokeFactory('Folder', id='pubrootonlyfolders')
        self.pubrootonlyfolders = self.folder.pubrootonlyfolders
        self.pubrootonlyfolders.invokeFactory('Folder', id='pubtest1-1')
        self.pubrootonlyfolders.invokeFactory('Folder', id='pubtest1-2')

        self.folder.invokeFactory('Folder', id='pubrootnonfolder')
        self.pubrootnonfolder = self.folder.pubrootnonfolder
        self.pubrootnonfolder.invokeFactory('Folder', id='pubtest2-1')
        self.pubrootnonfolder.invokeFactory('Document', id='pubtest2-2')
        
        #default page
        self.pubrootnonfolder.invokeFactory('Folder', id='pubtest_fld')
        self.pubrootnonfolder.invokeFactory('Document', id='pubtest_doc')
        setattr(self.pubrootnonfolder.pubtest_fld, 'default_page', 'pubtest_doc')

        self.folder.invokeFactory('Folder', id='deep')
        self.deep = self.folder.deep
        self.deep.invokeFactory('Folder', id='deep1')
        self.deep.deep1.invokeFactory('Folder', id='deep2')
        self.deep.deep1.deep2.invokeFactory('Document', id='deep3')

        self.folder.invokeFactory('Folder', id='topicroot')
        self.topicroot = self.folder.topicroot
        self.topicroot.invokeFactory('Topic', id='topicer')

        wf.doActionFor(self.pubrootonlyfolders, 'publish')
        wf.doActionFor(self.pubrootonlyfolders['pubtest1-1'], 'publish')
        wf.doActionFor(self.pubrootonlyfolders['pubtest1-2'], 'publish')

        wf.doActionFor(self.pubrootnonfolder, 'publish')
        wf.doActionFor(self.pubrootnonfolder['pubtest2-1'], 'publish')
        wf.doActionFor(self.pubrootnonfolder['pubtest2-2'], 'publish')
        wf.doActionFor(self.pubrootnonfolder['pubtest_fld'], 'publish')
        wf.doActionFor(self.pubrootnonfolder['pubtest_doc'], 'publish')

        wf.doActionFor(self.deep, 'publish')
        wf.doActionFor(self.deep.deep1, 'publish')
        # we don't publish deep2 because we want to test with it unpublished
        # we don't publish deep3 because we want to test with it unpublished

        wf.doActionFor(self.topicroot, 'publish')
        wf.doActionFor(self.topicroot.topicer, 'publish')

    def testAllPublishedFolders(self):
        brains = self.catalog.searchResults(getId='pubrootonlyfolders')
        self.assertEquals(brains[0].is_empty, True)

    def testAllPublishedNonFolder(self):
        brains = self.catalog.searchResults(getId='pubrootnonfolder')
        self.assertEquals(brains[0].is_empty, False)

    def testDeep(self):
        brains = self.catalog.searchResults(getId='deep')
        self.assertEquals(brains[0].is_empty, True)

        # the top level folder 'deep' should be reindexed when a document
        # a few levels down is published
        self.workflow.doActionFor(self.deep.deep1.deep2.deep3, 'publish')
        brains = self.catalog.searchResults(getId='deep')
        self.assertEquals(brains[0].is_empty, True)

        self.workflow.doActionFor(self.deep.deep1.deep2, 'publish')
        brains = self.catalog.searchResults(getId='deep')
        self.assertEquals(brains[0].is_empty, False)

    def testTopic(self):
        brains = self.catalog.searchResults(getId='topicroot')
        self.assertEquals(brains[0].is_empty, False)

    def testDefaultPage(self):
        brains = self.catalog.searchResults(getId='pubtest_fld')
        self.assertEquals(self.pubrootnonfolder.pubtest_fld.default_page, 'pubtest_doc')
        self.assertEquals(brains[0].is_empty, True)

def test_suite():
    import unittest
    return  unittest.TestSuite(unittest.makeSuite(TestCatalog))
