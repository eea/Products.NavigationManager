""" Catalog indexes
"""
import logging
from zope.interface import Interface
from zope.component.interfaces import ComponentLookupError
from plone.indexer import indexer
from Products.NavigationManager.sections.interfaces import (
    INavigationSectionPosition,
)

logger = logging.getLogger("Products.NavigationManager.catalog")
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
