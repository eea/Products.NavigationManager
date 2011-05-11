""" Navigation
"""
from zope.interface import implements, directlyProvides, providedBy
from zope.component import getMultiAdapter

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

#TODO: Plone4
#from Products.CMFPlone.browser.interfaces import INavigationPortlet
from Products.CMFPlone.browser.navigation import CatalogNavigationTabs
from Products.CMFPlone.browser.navtree import (
    DefaultNavtreeStrategy,
    NavtreeQueryBuilder,
)

from Products.NavigationManager.browser.buildtopictree import buildTopicTree
from Products.PloneLanguageTool.interfaces import ITranslatable
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
        is_empty = getattr(child['item'], 'is_empty', False)
        if child['currentItem'] or child['currentParent'] or not is_empty:
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
        context = utils.context(self)
        return '/'.join(getApplicationRoot(context).getPhysicalPath())

    def navigationTree(self):
        """ Tree
        """
        mContext = context = utils.context(self)
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

#TODO: Plone4  Fix me
#class NavigationManagerPortlet(NavigationPortlet):
    #""" EEA website navigation portlet fetches menu from navigation manager.
    #"""

    #implements(INavigationPortlet)

    #def __init__(self, context, request):
        #NavigationPortlet.__init__(self, context, request)
        #mship = getToolByName(context, 'portal_membership')
        #isAnonymous = mship.isAnonymousUser()
        #if isAnonymous:
            #root = getMenu(context)
            #if root is not None:
                #self._root = [ root ]

    #def title(self):
        #return self.navigationRoot().Title()

    #def navigationRoot(self):
        #""" Override """
        #if not utils.base_hasattr(self, '_root'):
            #self._root = [ NavigationPortlet.navigationRoot(self) ]
        #return self._root[0]

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

class NavtreeManagerQueryBuilder:
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
        return DefaultPage.isDefaultPage(self,
                            obj, context_) and obj.exclude_from_nav() or False

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
        for node in ntool.getTree(site, tabselected):
            item = node.get('item', {})

            data = {
                'name': item.get('title', '<NOT SET>'),
                'id': item.get('id', '_not_set_'),
                'url': item.get('url', '#'),
                'description': item.get('description', '<NOT SET>'),
            }
            result.append(data)
        return result
