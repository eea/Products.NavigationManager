""" Sections interfaces
"""
from zope.interface import Interface, Attribute

class INavigationSectionPositionable(Interface):
    """ Marker interface for content objects that can be positioned in
        navigation sections. """

class INavigationSectionPosition(Interface):
    """ Navigation Section adapters
    """
    section = Attribute(u"Navigation section")

class INavigationSections(Interface):
    """ Navigation Sections adapters
    """
    left = Attribute(u"Left navigation sections")
    right = Attribute(u"Right navigation sections")
