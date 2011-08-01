""" Catalog indexes
"""
import logging
from zope.interface import Interface
from zope.component.interfaces import ComponentLookupError
from plone.indexer import indexer
from Products.CMFPlone.utils import base_hasattr, safe_callable
from Products.NavigationManager.sections.interfaces import (
    INavigationSectionPosition,
)

logger = logging.getLogger("Products.NavigationManager.catalog")

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

#
# New ZCatalog indexes
#
@indexer(Interface)
def getNavSectionsForIndex(obj, **kwargs):
    """ Get navigation section for index
    """
    try:
        nav = INavigationSectionPosition(obj)
        return nav.section
    except (ComponentLookupError, TypeError, ValueError):
        raise AttributeError
