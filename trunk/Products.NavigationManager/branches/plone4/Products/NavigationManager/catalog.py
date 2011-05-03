from zope.interface import Interface
from plone.indexer import indexer
from Acquisition import aq_parent, aq_inner
from OFS.Application import Application
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.Portal import PloneSite
from Products.CMFPlone.utils import base_hasattr, safe_callable
from p4a.subtyper.interfaces import ISubtyper
from zope.component import getUtility
import logging
logger = logging.getLogger("Products.NavigationManager.catalog")

def canBeEmpty(obj):
    """ figures out whether the object can be treaded as empty or not.
        Non-folderish objects can not be empty. Topics are dynamic so
        they can not be empty either. """

    props = getToolByName(obj, 'portal_properties')
    site_props = getattr(props, 'site_properties')
    hide_if_empty = getattr(site_props, 'hide_if_empty', ())

    # Handle subtyped objects
    unhide_subtypes = getattr(site_props, 'unhide_subtypes', ())
    subtyper = getUtility(ISubtyper)
    etype = subtyper.existing_type(obj)
    type_name = etype and etype.name or ""
    return obj.portal_type in hide_if_empty and \
           type_name not in unhide_subtypes

def indexObject(obj):
    """ Adds an object to the catalog if it's not already there.
        It only adds contentish objects by checking if the object
        has an indexObject method. Taken from CMFPlone/CatalogTool.py
    """
    if (base_hasattr(obj, 'indexObject') and safe_callable(obj.indexObject)):
        try:
            obj.indexObject()
        except TypeError, err:
            # Catalogs have 'indexObject' as well, but they
            # take different args, and will fail
            logger.info(err)

def indexChildrenIfNotIndexed(obj, catalog):
    # check if there are objects that are not yet indexed
    # this should only happen when we do catalog update/rebuild in zmi
    for child in obj.objectValues():
        path = '/'.join(child.getPhysicalPath())
        if catalog.getrid(path) is None:
            # the object doesn't exist in catalog, so add it
            indexObject(child)

@indexer(Interface)
def getEmptyForIndex(obj, portal, **kwargs):
    can_be_empty = canBeEmpty(obj)

    if not can_be_empty:
        return False

    listing_views = ('folder_listing', 'folder_summary_view', 'topic_view',
                     'richtopic_view', 'atct_album_view', 'folder_tabular_view',
                     'folder_contents', 'mediacentre_view')
    if base_hasattr(obj, 'layout') and obj.getLayout() not in listing_views:
        return False

    if base_hasattr(obj, 'default_page'):
        page = obj.getDefaultPage()
        if page is not None:
            page = getattr(obj, obj.getDefaultPage(), None)
        if page is not None and not canBeEmpty(page):
            return False

    catalog = getToolByName(portal, 'portal_catalog')
    query = {'path': {'query': '/'.join(obj.getPhysicalPath()), 'depth': 1},
             'review_state': 'published' }
    portal_languages = getToolByName(portal, 'portal_languages', None)

    # the request might not contain the right language if reindexing
    # is done programmatically
    # because the results of the catalog query is language specific,
    # we need to enable language support for each object that is reindexed,
    # an "english"  view might create and reindex objects under /www/sv
    # such objects need to add Language='sv' to the query
    if portal_languages:
        old_namestack = portal.REQUEST.get('TraversalRequestNameStack', [])
        namestack = list(obj.getPhysicalPath()[2:])
        namestack.reverse()
        portal.REQUEST.set('TraversalRequestNameStack', namestack)
        portal_languages.setLanguageBindings()


    if getattr(obj, 'portal_type', None) in ('Topic', 'RichTopic'):
        if obj.queryCatalog(batch=True):
            return False
        else:
            return True

    indexChildrenIfNotIndexed(obj, catalog)
    brains = catalog.searchResults(query)
    if portal_languages:
        portal.REQUEST.set('TraversalRequestNameStack', old_namestack)
        portal_languages.setLanguageBindings()

    for brain in brains:
        if brain.getURL() == obj.absolute_url():
            # we don't care about the object that is just being reindexed
            continue

        if not canBeEmpty(brain.getObject()) or not brain.is_empty:
            # if we find a non-folder object, then the object is not empty
            return False

    return True

def reindexTree(obj):
    obj.reindexObject(idxs=['is_empty'])
    while not isinstance(obj, PloneSite):
        obj = aq_parent(aq_inner(obj))
        obj.reindexObject(idxs=['is_empty'])

def updateTopics(obj):
    portal_type = ['Topic', 'RichTopic']
    if getattr(obj, 'portal_type', None) not in portal_type:
        catalog = getToolByName(obj, 'portal_catalog', None)
        for b in catalog(portal_type=portal_type,
                         is_empty=True):
            reindexTree(b.getObject())

def objectAdded(obj, event):
    # tell the parent about this, maybe it was marked as empty before
    portal_factory = getToolByName(obj, 'portal_factory', None)
    if portal_factory and not portal_factory.isTemporary(obj):
        reindexTree(event.newParent)

def objectRemoved(obj, event):
    # tell the parent to check itself whether it should be marked as empty
    if not isinstance(event.oldParent, Application):
        reindexTree(event.oldParent)

def workflowStateChanged(obj, event):
    # first reindex current object because its workflow change is not
    # yet reflected by the catalog - the parents need this information
    obj.reindexObject()
    if not isinstance(obj, PloneSite):
        parent = aq_parent(aq_inner(obj))
        reindexTree(parent)

def objectModified(obj, event):
    updateTopics(obj)
    reindexTree(obj)
