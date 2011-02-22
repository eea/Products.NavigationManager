# -*- coding: utf-8 -*-

from Products.NavigationManager.tests.NavigationManagerTestCase import NavigationManagerTestCase
from zope.app.component.hooks import setSite
from zope.app.event.objectevent import ObjectModifiedEvent
from zope.event import notify
from Products.NavigationManager.browser import menu

class TestMenu(NavigationManagerTestCase):
    """ Test-cases for class(es) relations. """

    def afterSetUp(self):
        setSite(self.portal)
        self.setRoles('Manager')

        self.folder.invokeFactory('Folder', id='pubrootonlyfolders')
        self.pubrootonlyfolders = self.folder.pubrootonlyfolders
        self.pubrootonlyfolders.invokeFactory('Folder', id='pubtest1-1')
        self.pubrootonlyfolders.invokeFactory('Folder', id='pubtest1-2')

        wf = self.workflow = self.portal.portal_workflow
        wf.doActionFor(self.pubrootonlyfolders, 'publish')
        wf.doActionFor(self.pubrootonlyfolders['pubtest1-1'], 'publish')
        wf.doActionFor(self.pubrootonlyfolders['pubtest1-2'], 'publish')

    def testDefaultNavigationManagerPath(self):
        m = menu.Menu(self.pubrootonlyfolders['pubtest1-2'], self.portal.REQUEST)
        path = [ folder['id'] for folder in m.getPath()]
        self.assertEquals(path, ['Members', 'test_user_1_', 'pubrootonlyfolders'])


def test_suite():
    import unittest
    return  unittest.TestSuite(unittest.makeSuite(TestMenu))
