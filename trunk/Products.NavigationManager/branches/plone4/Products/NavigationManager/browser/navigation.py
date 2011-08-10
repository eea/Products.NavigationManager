""" Navigation
"""
from zope.interface import implements, directlyProvides, providedBy
from zope.component import getMultiAdapter, queryAdapter
from zope.schema.vocabulary import SimpleTerm

from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from Products.Five.browser import BrowserView

from plone.app.layout.navigation.defaultpage import DefaultPage
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.layout.navigation.interfaces import (
    INavtreeStrategy,
    INavigationQueryBuilder,
    INavigationRoot,
    IDefaultPage
)

from plone.app.portlets.portlets.navigation import NavtreeStrategy
from plone.app.portlets.portlets.navigation import Renderer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.browser.navigation import CatalogNavigationTabs
from Products.CMFPlone.browser.navtree import (
    DefaultNavtreeStrategy,
    NavtreeQueryBuilder,
)

from Products.NavigationManager.browser.buildtopictree import buildTopicTree
from Products.PloneLanguageTool.interfaces import ITranslatable
from Products.NavigationManager.sections.interfaces import INavigationSections
from Products.NavigationManager.browser.interfaces import (
    INavigationManagerRequest,
    INavigationManagerTree,
)

def getApplicationRoot(obj):
    """ Application Root
    """
    portal_url = getToolByName(obj, 'portal_url')
    portal = portal_url.getPortalObject()

    while not INavigationRoot.providedBy(obj) and (
        aq_base(obj) is not aq_base(portal)):
        obj = utils.parent(obj)

    return obj

def getMenu(context):
    """ Get Menu
    """
    menuid = getattr(context, 'navigationmanager_menuid', None)
    submenu = getattr(context, 'navigationmanager_submenu', None)
    if menuid is None or submenu == 'plone navigation':
        return None

    catalog = getToolByName(context, 'portal_catalog')
    query = { 'portal_type' : 'NavigationItem' }
    if menuid is not None:
        query['id'] = menuid
    else:
        query['getUrl'] = context.absolute_url()
    if (ITranslatable.isImplementedBy(context) and
        context.Language() is not None and len(context.Language())) > 0:
        query['Language'] = context.Language()
    menuItems = catalog.searchResults( query )

    if len(menuItems) > 0:
        navmanager = getToolByName(context, 'portal_navigationmanager')
        obj = menuItems[0].getObject()
        prev = obj
        while aq_base(utils.parent(obj)) is not aq_base(navmanager):
            prev = obj
            obj = utils.parent(obj)
        return prev
    return None

def getCurrentItem(tree):
    """ Get current item
    """
    for child in tree['children']:
        if child['currentParent']:
            return getCurrentItem(child)
        elif child['currentItem']:
            return child, tree

def removeEmptyFolders(tree):
    """ Remove all empty folders on the first level in the tree
    """
    new_children = []
    for child in tree['children']:
        if child['currentItem'] or child['currentParent']:
            new_children.append(child)
    tree['children'] = new_children

    # recursively remove all empty folders lower down in the hierarchy
    for child in tree['children']:
        removeEmptyFolders(child)

class ListAllNode:
    """ This is an object that pretends to be a brain. """

    Title = 'List all'
    portal_type = 'Document'
    review_state = 'published'
    getUrl = 'atct_topic_full_view'

    def getPath(self):
        """ Path
        """
        return 'dd'

    def getURL(self):
        """ URL
        """
        return 'atct_topic_full_view'

    def getRemoteUrl(self):
        """ Remote URL
        """
        return None

    def Creator(self):
        """ Creator
        """
        return ''

    def Description(self):
        """ Description
        """
        return ''

class NavigationManagerTree(BrowserView):
    """ Navigation Tree which combines Navigation Manager menu and plone
        default. """

    implements(INavigationManagerTree)

    def navigationTreeRootPath(self):
        """ Tree root path
        """
        context = self.context
        return '/'.join(getApplicationRoot(context).getPhysicalPath())

    def navigationTree(self):
        """ Tree
        """
        mContext = context = self.context
        menu = getMenu(context)
        strategy = None
        queryBuilder = None
        isAnon = getToolByName(context, 'portal_membership').isAnonymousUser()

        if menu and isAnon:
            mContext = menu
            queryBuilder = NavtreeManagerQueryBuilder(mContext)

        if queryBuilder is None:
            queryBuilder = INavigationQueryBuilder(mContext)

        query = queryBuilder()

        root = getApplicationRoot(context)
        if ITranslatable.isImplementedBy(root):
            query['Language'] = root.getLanguage()

        # Logged in users should get all objects in the navtree,
        # independent of the workflow state.
        if not isAnon:
            if query.has_key('review_state'):
                del query['review_state']

        query['is_default_page'] = {'query' : (True, False),
                                    'operator': 'or' }


        strategy = getMultiAdapter((mContext, self), INavtreeStrategy)
        reqInterfaces = providedBy(context.REQUEST)
        directlyProvides(context.REQUEST,
                         reqInterfaces + INavigationManagerRequest)
        tree = buildFolderTree(mContext,
                               obj=mContext, query=query, strategy=strategy)
        props = getToolByName(context, 'portal_properties')
        navtree_props = getattr(props, 'navtree_properties', None)
        if navtree_props is not None:
            topic_enabled = navtree_props.getProperty(
                'topicListingInNavtree', False)
        else:
            topic_enabled = False

        portal_factory = getToolByName(mContext, 'portal_factory')
        temporary = portal_factory.isTemporary(mContext)

        # if context is a Smart Folder, then the navtree should display
        # the result of the smart folder query instead of folder contents

        if mContext.portal_type.endswith('Topic') and topic_enabled and \
                not temporary:
            topictree = buildTopicTree(mContext,
                                       obj=mContext, strategy=strategy)

            current, parent = getCurrentItem(tree)
            topiccurrent, _topicparent = getCurrentItem(topictree)
            if isAnon:
                parent['children'] = topiccurrent['children']
            else:
                parent['children'] = [current]
                current['children'] = topiccurrent['children']

            item = ListAllNode()
            listAllNode = {'item'      : item,
                           'depth'         : 0,  # irrelevant
                           'currentItem'   : False,
                           'currentParent' : False,
                           'children': [] }

            if strategy is not None:
                listAllNode = strategy.decoratorFactory(listAllNode)

            topiccurrent['children'].append(listAllNode)

        directlyProvides(context.REQUEST, reqInterfaces)
        for m in tree['children']:
            if menu:
                m['getURL'] = m['item']['getUrl']
            selectedMenuId = getattr(context, 'navigationmanager_menuid', None)
            currentContext = m['getURL'] == context.absolute_url()

            currentMenuItem = (selectedMenuId and
                               m['item']['getId'] == selectedMenuId)

            m['currentItem'] = (currentContext or currentMenuItem
                                or m['currentItem'] and not m['currentParent'])

            if m['currentParent']:
                for child in m['children']:
                    if child['defaultPage']:
                        idx = m['children'].index(child)
                        m['children'].pop(idx)
                        m['children'].insert(0, child)
                        break

            if m.get('defaultPage', False):
                idx = tree['children'].index(m)
                tree['children'].pop(idx)
                tree['children'].insert(0, m)

        # anonymous users don't want to see empty folders
        if isAnon and not menu:
            removeEmptyFolders(tree)
        return tree

class NavtreeManagerStrategy(DefaultNavtreeStrategy):
    """ The navtree strategy used for the default navigation portlet and
        respects NavigationManager submenu as root.  """

    implements(INavtreeStrategy)

    def __init__(self, context, view=None):
        DefaultNavtreeStrategy.__init__(self, context, view)
        self.rootPath = '/'.join(context.getPhysicalPath())
        self.showAllParents = False

class NavtreeSectionStrategy(DefaultNavtreeStrategy):
    """ The navtree strategy that provides navigation
        section info for each node.
    """

    def decoratorFactory(self, node):
        """ Decorator factory
        """
        newNode = DefaultNavtreeStrategy.decoratorFactory(self, node)
        item = node['item']
        newNode['navSection'] = getattr(item, 'navSection', None) or 'default'
        newNode['defaultPage'] = getattr(item, 'is_default_page', False)
        return newNode

class TopicNavtreeStrategy(NavtreeSectionStrategy):
    """ The navtree strategy for topics. """

    def __init__(self, context, view=None):
        super(TopicNavtreeStrategy, self).__init__(self, context, view)
        if view is not None:
            self.rootPath = view.navigationTreeRootPath()
        else:
            self.rootPath = getNavigationRoot(context)
        self.showAllParents = True

    def decoratorFactory(self, node):
        """ Decorator factory
        """
        newNode = NavtreeSectionStrategy.decoratorFactory(self, node)
        item = node['item']
        newNode['defaultPage'] = getattr(item, 'is_default_page', False)
        return newNode

class NavtreeManagerQueryBuilder(object):
    """Build a navtree query based on the settings in navtree_properties
    """
    implements(INavigationQueryBuilder)

    def __init__(self, context):
        portal_properties = getToolByName(context, 'portal_properties')
        #portal_url = getToolByName(context, 'portal_url')
        navtree_properties = getattr(portal_properties, 'navtree_properties')

        query = {}
        rootPath = currentPath = '/'.join(context.getPhysicalPath())

        # If we are above the navigation root, a navtree query would return
        # nothing (since we explicitly start from the root always). Hence,
        # use a regular depth-1 query in this case.

        if not currentPath.startswith(rootPath):
            query['path'] = {'query' : rootPath, 'depth' : 2}
        else:
            query['path'] = {'query' : currentPath, 'navtree' : 2}

        # portal/portal_navigationmanager/site/menu = 4
        query['path']['navtree_start'] = 4

        # XXX: It'd make sense to use 'depth' for bottomLevel, but it doesn't
        # seem to work with EPI.

        # Only list the applicable types
        query['portal_type'] = utils.typesToList(context)

        # Apply the desired sort
        sortAttribute = navtree_properties.getProperty('sortAttribute', None)
        if sortAttribute is not None:
            query['sort_on'] = sortAttribute
            sortOrder = navtree_properties.getProperty('sortOrder', None)
            if sortOrder is not None:
                query['sort_order'] = sortOrder

        # Filter on workflow states, if enabled
        if navtree_properties.getProperty('enable_wf_state_filtering', False):
            query['review_state'] = navtree_properties.getProperty(
                'wf_states_to_show', ())

        self.query = query

    def __call__(self):
        return self.query


class NavtreeManagerQueryBuilderForSections(NavtreeQueryBuilder):
    """ Navtree manager query builder for sections
    """
    def __init__(self, context):
        NavtreeQueryBuilder.__init__(self, context)
        if self.query.get('depth', None) is not None:
            self.query['depth'] = 2
        else:
            self.query['navtree'] = 2


class DefaultPageIsNormalPage(DefaultPage):
    """ Default page is only hidden if it's excluded from navigation. """
    implements(IDefaultPage)

    def isDefaultPage(self, obj, context_=None):
        """ Default page?
        """
        if DefaultPage.isDefaultPage(self, obj, context_):
            return obj.exclude_from_nav()
        return False
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

    def getNavTree(self, _marker=None):
        """ getNavTree section aware
        """
        if not self._tree:
            queryBuilder = getMultiAdapter(
                (self.root, self.data), INavigationQueryBuilder)

            strategy = getMultiAdapter(
                (self.root, self.data), INavtreeStrategy)

            self._tree = buildFolderTree(self.root, obj=self.context,
                                        query=queryBuilder(), strategy=strategy)

        return self._tree

    def createNavTree(self, section='default'):
        """ createNavTree section aware
        """
        data = self.getNavTree()
        children = [child for child in data.get('children', [])
                    if child.get('navSection', '') == section]

        bottomLevel = self.data.bottomLevel or self.properties.getProperty(
            'bottomLevel', 0)

        return self.recurse(children=children, level=1, bottomLevel=bottomLevel)

    def createNavSection(self, section='default', label='Menu'):
        """ Render navigations section
        """
        return self.section(section=section, sectionTitle=label)
