""" Navigation
"""
from zope.interface import implements
from zope.component import getMultiAdapter, queryAdapter
from zope.schema.vocabulary import SimpleTerm

from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils

from Products.NavigationManager.browser.navtree import buildFolderTree
from plone.app.layout.navigation.interfaces import (
    INavtreeStrategy,
    INavigationQueryBuilder,
    INavigationRoot,
)

from plone.app.portlets.portlets.navigation import NavtreeStrategy
from plone.app.portlets.portlets.navigation import QueryBuilder
from plone.app.portlets.portlets.navigation import Renderer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.browser.navigation import CatalogNavigationTabs
from Products.NavigationManager.sections.interfaces import INavigationSections

def getApplicationRoot(obj):
    """ Application Root
    """
    portal_url = getToolByName(obj, 'portal_url')
    portal = portal_url.getPortalObject()

    while not INavigationRoot.providedBy(obj) and (
        aq_base(obj) is not aq_base(portal)):
        obj = utils.parent(obj)

    return obj

class ListAllNode(object):
    """ This is an object that pretends to be a brain. """

    portal_type = 'Document'
    review_state = 'published'
    getUrl = 'folder_listing'
    getId = 'list-all'
    getIcon = 'document_icon.png'

    def __getitem__(self, name, default=None):
        return getattr(self, name, default)

    def Title(self):
        """ Title
        """
        return 'List all'

    def Description(self):
        """ Description
        """
        return 'List all items'

    def Creator(self):
        """ Creator
        """
        return ''

    def UID(self):
        """ UID
        """
        return ''

    def getPath(self):
        """ Path
        """
        return self.getUrl

    def getURL(self):
        """ URL
        """
        return self.getUrl

    def getRemoteUrl(self):
        """ Remote URL
        """
        return None
#
# Override plone default behaviour
#
class PortalNavigationTabs(CatalogNavigationTabs):
    """ Portal Tabs
    """
    def topLevelTabs(self, actions=None, category='portal_tabs'):
        """ Top level tabs
        """
        ntool = getToolByName(self.context, 'portal_navigationmanager', None)
        if not ntool:
            return super(PortalNavigationTabs, self).topLevelTabs(
                actions, category)

        site = getattr(self.context, 'navigationmanager_site', 'default')
        tabselected = getattr(self.context, 'navigationmanager_menuid',
                              'default')

        result = []
        for node in ntool.getTree(site, tabselected, recursive=False):
            item = node.get('item', {})

            data = {
                'name': item.get('title', '<NOT SET>'),
                'id': item.get('id', '_not_set_'),
                'url': item.get('url', '#'),
                'description': item.get('description', '<NOT SET>'),
            }
            result.append(data)
        return result
#
# Navigation portlet
#
class SectionAwareQueryBuilder(QueryBuilder):
    """ Navigation tree section aware query builder
    """
    @property
    def navtree_start(self):
        """ Level to start navigation tree
        """
        return len(self.context.getPhysicalPath()) - 1

    def __call__(self):
        mtool = getToolByName(self.context, 'portal_membership')
        if mtool.isAnonymousUser():
            self.query['review_state'] = 'published'
        self.query['path']['navtree_start'] = self.navtree_start
        return self.query

class SectionAwareNavStrategy(NavtreeStrategy):
    """ Navigation tree section aware strategy
    """
    implements(INavtreeStrategy)

    def decoratorFactory(self, node):
        """ Add custom properties to tha navigation tree node
        """
        newNode = super(SectionAwareNavStrategy, self).decoratorFactory(node)
        item = node.get('item', None)
        section = getattr(item, 'navSection', None) or 'default'
        newNode['navSection'] = section
        is_default_page = getattr(item, 'is_default_page', False)
        newNode['is_default_page'] = is_default_page

        # List all item
        if isinstance(item, ListAllNode):
            ptool = getToolByName(self.context, 'portal_properties')
            ntool = getattr(ptool, 'navtree_properties')

            listAllTemplate = ntool.getProperty(
                'listAllTemplate', '') or 'folder_listing'
            item.getUrl = listAllTemplate

            url = '/'.join((self.context.absolute_url(), item.getUrl))
            newNode['absolute_url'] = url
            newNode['getURL'] = url

        return newNode

class NavigationRenderer(Renderer):
    """ Custom renderer for navigation portlet
    """
    _template = ViewPageTemplateFile('templates/navigation.pt')
    recurse = ViewPageTemplateFile('templates/navigation_recurse.pt')
    section = ViewPageTemplateFile('templates/section.pt')

    def __init__(self, context, request, view, manager, data):
        super(NavigationRenderer, self).__init__(
            context, request, view, manager, data)
        self.root = getApplicationRoot(self.context)
        self._tree = {}

    @property
    def sections(self):
        """ Navigation portlet sections
        """
        yield SimpleTerm('default', 'default', 'Menu')
        sections = queryAdapter(self.context, INavigationSections)
        if not sections:
            return

        for section in sections.left:
            yield section

    @property
    def bottomLevel(self):
        """ Navigation tree bottom level
        """
        return self.data.bottomLevel or self.properties.getProperty(
            'bottomLevel', 0)

    @property
    def maxChildren(self):
        """ Maximum children before 'List all' link
        """
        return self.properties.getProperty('maxChildren', 0)

    def display(self, section='default'):
        """ Display section
        """
        tree = self.getNavTree()
        for child in tree.get('children', []):
            if child.get('navSection', '') == section:
                return True
        return False

    def getNavRootPath(self):
        """ Tree root path
        """
        return '/'.join(self.root.getPhysicalPath())

    def apply_maxChildren(self, tree, context=None):
        """ Apply maxChildren on tree
        """
        maxChildren = self.maxChildren
        if maxChildren <= 0:
            return tree

        children = tree.get('children', [])

        if len(children) <= (maxChildren + maxChildren * 0.20): # orphans
            return tree

        newChildren = []
        for index, child in enumerate(children):
            # Always include current item/parent
            if child.get('currentParent', False
                         ) or child.get('currentItem', False):
                newChildren.append(child)
                continue

            if index >= maxChildren:
                continue

            newChildren.append(child)

        # List all node
        item = ListAllNode()
        listAllNode = {
            'item': item,
            'depth': 1,  # irrelevant
            'currentItem': False,
            'currentParent': False,
            'children': []
        }

        strategy = getMultiAdapter((context, self.data), INavtreeStrategy)
        listAllNode = strategy.decoratorFactory(listAllNode)

        newChildren.append(listAllNode)

        tree['children'] = newChildren
        return tree

    def getRecursiveNavTree(self, root=None, depth=1):
        """ Recurse to get context children
        """
        if not root:
            root = self.root

        bottomLevel = self.bottomLevel
        if bottomLevel and depth > bottomLevel:
            return {'children': []}

        queryBuilder = getMultiAdapter(
                (root, self.data), INavigationQueryBuilder)

        strategy = getMultiAdapter(
            (root, self.data), INavtreeStrategy)

        tree = buildFolderTree(root, obj=self.context,
                               query=queryBuilder(), strategy=strategy)

        for child in tree.get('children', []):
            if not child.get('show_children', False):
                continue

            if not (child.get('currentParent', False) or
                    child.get('currentItem', False)):
                continue

            brain = child.get('item', None)
            doc = brain.getObject()

            # Avoid infinite recursion
            if doc == root:
                tree['children'] = child.get('children', [])
                break

            childtree = self.getRecursiveNavTree(doc, depth=depth+1)
            childtree = self.apply_maxChildren(childtree, context=doc)
            child['children'] = childtree.get('children', [])

        return tree

    def getNavTree(self, _marker=None):
        """ getNavTree section aware
        """
        if not self._tree:
            self._tree = self.getRecursiveNavTree(self.root)
        return self._tree

    def createNavTree(self, section='default'):
        """ createNavTree section aware
        """
        data = self.getNavTree()
        children = [child for child in data.get('children', [])
                    if child.get('navSection', '') == section]

        return self.recurse(children=children, level=1,
                            bottomLevel=self.bottomLevel)

    def createNavSection(self, section='default', label='Menu'):
        """ Render navigations section
        """
        return self.section(section=section, sectionTitle=label)
