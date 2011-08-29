""" Navigation
"""
from zope.interface import implements
from zope.component import getMultiAdapter, queryAdapter
from zope.schema.vocabulary import SimpleTerm

from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils

from plone.app.layout.navigation.navtree import buildFolderTree
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
        self.query['path']['navtree_start'] = self.navtree_start
        self.query['is_default_page'] = {
            'query': [False, True],
            'operator': 'or'
        }
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

    def fix_defaultpage_position(self, tree):
        """ Fix default page position
        """
        for index, child in enumerate(tree.get('children', [])):
            if child.get('is_default_page', False):
                tree['children'].pop(index)
                tree['children'].insert(0, child)
                break
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
        tree = self.fix_defaultpage_position(tree)

        for child in tree.get('children', []):
            if not child.get('show_children', False):
                continue

            if not (child.get('currentParent', False) or
                    child.get('currentItem', False)):
                continue

            brain = child.get('item', None)
            doc = brain.getObject()
            childtree = self.getRecursiveNavTree(doc, depth=depth+1)
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
