""" Event handlers
"""
from Products.NavigationManager.sections.interfaces import (
    INavigationSectionPosition,
)

def objectNavigationSet(obj, event):
    """ Checks if the object's navigations section are modified.
    If true, catalog is updated.
    """
    for desc in event.descriptions:
        if desc.interface == INavigationSectionPosition:
            obj.reindexObject()
            break
