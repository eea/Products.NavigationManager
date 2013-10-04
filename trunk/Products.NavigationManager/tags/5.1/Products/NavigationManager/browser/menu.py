""" Menu
"""
import zope.interface

from Acquisition import aq_parent, aq_inner, aq_base
from Products.CMFCore.interfaces._content import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory

from Products.Five.browser import BrowserView
from Products.NavigationManager.browser.interfaces import IMenu
from zope.component import getMultiAdapter

class Menu(BrowserView):
    """ EEA Menu Navigation View """
    zope.interface.implements(IMenu)

    def getSiteRootId(self):
        """ returns the id of the site root content folder """
        obj = self.context
        while obj and not ISiteRoot.providedBy(obj):
            base = aq_base(obj)
            site = getattr(base, 'navigationmanager_site', None)
            if site:
                return base.getId()
            obj = aq_parent(aq_inner(obj))
        # we fall back on 'SITE' if we don't find any object that has the
        # navigationmanager_site property, while we traverse up to the root
        return 'SITE'

    def getSubMenu(self, site='default', menuid=''):
        """ Returns a list of dictionaries with nav info about this node """

        navManager = getToolByName(self.context, 'portal_navigationmanager')
        tree = navManager.getTree(site)

        #initialise variables
        menuitems = []
        result = []
        parent_node = ''

        #find submenu with id == menuid,
        #it does this only in 2 sublevels
        for submenu in tree:
            if submenu['item']['id'] == menuid:
                parent_node = submenu
                menuitems = submenu['children']
            #else check 3rd level
            else:
                for child in submenu['children']:
                    if child['item']['id'] == menuid:
                        parent_node = child
                        menuitems = child['children']

        # add the parent node as first node
        if parent_node:
            result.append(self.buildNode(parent_node,'dummyid') )

        # Assign an empty list to index 1 for the loop below
        result.append([])

        # loop through all nodes
        for m in menuitems:

            node = (self.buildNode(m, menuid))
            # level 3 menu
            daycare = node['children']
            node['children'] = \
                    [ self.buildNode(childe, menuid) for childe in daycare ]

            result[1].append(node)

        return result

    def getPath(self, site='default', menuid=''):
        """ Given a menuid or object, it returns a list of dictionaries
            with path nav info (breadcrumbs) """

        catalog = getToolByName(self.context, 'portal_catalog')
        language = self.request.get('LANGUAGE', 'en')

        navManager = getToolByName(self.context, 'portal_navigationmanager')

        siteobj = getattr(navManager, site, None)

        if siteobj is not None:
            if language != 'en'  and siteobj.hasTranslation(language):
                siteobj = siteobj.getTranslation(language)
                site = siteobj.getId()


        bpath = []
        menuobj = None
        if menuid == '':
            bpath = self.createObjPathFromObject(self.context)
        else:
            #find menuitem with id=menuid
            menubrains = catalog(getId = menuid,
                               portal_type = 'NavigationItem',
                               Language = language)
            if not menubrains:
                menubrains = catalog(getId = menuid,
                               portal_type = 'NavigationItem',
                               Language = 'en')

            if menubrains:
                menuobj = menubrains[0].getObject()
                #create the base path for menuobj
                bpath = self.createPathFromObject(site, menuobj)


        homeobj = False
        if siteobj is not None:
            if hasattr(siteobj, 'home'):
                siteobj = getattr(siteobj, 'home')
                homeobj = True
        if  homeobj:
            home_title = siteobj.Title()
        else:
            home_title = PloneMessageFactory('Home')
        # create first item Home (=first item of navmanager)
        # and insert on start of path
        if siteobj is not None:
            home = { 'id' : siteobj.getId(),
                     'url' : siteobj.getUrl(),
                     'title' : home_title,
                     'description' : siteobj.Description()}
            bpath.insert(0, home)

        return bpath

    def createPathFromObject(self, site, menuobj):
        ''' given a menuobj, it returns a list of dictionaries for
        global base path '''
        #navManager = getToolByName(self.context, 'portal_navigationmanager')
        #parents_ids = []

        path = []
        while menuobj and menuobj.getId() != site and \
                menuobj.getId() != 'portal_navigationmanager':
            path.insert(0, { 'id' : menuobj.getId(),
                          'url' : menuobj.getUrl(),
                          'title' : menuobj.Title(),
                          'description' : menuobj.Description()})
            menuobj = aq_parent(menuobj)

        return path

    def createObjPathFromObject(self, obj):
        ''' given an obj, it returns a list of dictionaries for global
        base path '''
        path = []
        if getattr(aq_parent(aq_inner(obj)), 'portal_type', 'Plone Site') \
        == 'Plone Site':
            return []

        obj = aq_parent(aq_inner(obj))

        # if we are outside plone we don't have portal_type
        while obj and getattr(obj, 'portal_type', 'Plone Site') != 'Plone Site':
            path.insert(0, { 'id' : obj.getId(),
                          'url' : obj.absolute_url(),
                          'title' : obj.Title(),
                          'description' : obj.Description()})
            obj = aq_parent(aq_inner(obj))

        return path

    def isRoot(self):
        """ Root?
        """
        if hasattr(self.context, 'getCanonical') and \
                self.context.getCanonical().getId() == 'SITE':
            return True

        parent = aq_parent(aq_inner(self.context))
        plone_view = getMultiAdapter((self.context, self.request),
                name = "plone")
        if hasattr(parent, 'getCanonical') and \
                parent.getCanonical().getId() == 'SITE' and \
                plone_view.isDefaultPageInFolder():
            return True

        return False

    def buildNode(self, menuitem, menuid):
        ''' takes one node and builds the dictionary of information. '''
        children = menuitem['children']
        m = menuitem['item']

        return  { 'id' : m['id'],
                'url' : m['url'],
                'title' : m['title'],
                'description' : m['description'],
                'currentItem' : m['id'] == menuid ,
                'children' : children }

    def getItemUrl(self, url, relative='no'):
        ''' given a url, it returns absolute or relative url '''
        if relative == 'yes':
            httpfound = url.find('http')>-1
            # find first slash after the http
            idx1 = url.find('/', 9)
            if httpfound and idx1 > -1:
                return url[idx1:]
            elif httpfound and idx1 < 0:
                #case of http://site.eu
                return '/'
            else:
                # special case. if here then url doesn't start with http.
                #(we should not have non-http or relative urls in navigation
                #manager anyway)
                return url
        else:
            return url


