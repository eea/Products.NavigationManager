""" Sections
"""
from persistent.dict import PersistentDict
from zope.event import notify
from zope.interface import Interface, Attribute, implements
from zope.component import adapts
from zope.component.interfaces import ComponentLookupError
from zope.annotation.interfaces import IAnnotations
from zope.lifecycleevent import ObjectModifiedEvent, Attributes
from zope.schema.vocabulary import SimpleTerm
from plone.indexer import indexer
from Products.PloneLanguageTool.interfaces import ITranslatable

KEY = "NavigationManager"

class INavigationSectionPositionable(Interface):
    """ Marker interface for content objects that can be positioned in
        navigation sections. """

class INavigationSectionPosition(Interface):
    section = Attribute(u"Navigation section")

class INavigationSections(Interface):
    left = Attribute(u"Left navigation sections")
    right = Attribute(u"Right navigation sections")

class NavigationSectionPosition(object):
    implements(INavigationSectionPosition)
    adapts(INavigationSectionPositionable)

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        mapping = annotations.get(KEY)
        if mapping is None:
            section =  { 'section': None }
            mapping = annotations[KEY] = PersistentDict(section)
        self.mapping = mapping

    @property
    def section(self):
        anno = IAnnotations(self.context)
        mapping = anno.get(KEY)
        return mapping['section']

    @section.setter
    def section(self, value):
        anno = IAnnotations(self.context)
        mapping = anno.get(KEY)
        mapping['section'] = value
        info = Attributes(INavigationSectionPosition, 'section')
        notify(ObjectModifiedEvent(self.context, info))

class NavigationSections(object):
    implements(INavigationSections)
    adapts(Interface)

    def __init__(self, context):
        if ITranslatable.providedBy(context):
            self.context = context.getCanonical()
        else:
            self.context = context

    def _createSectionList(self, sectionLines):
        sections = []
        if sectionLines:
            for section in sectionLines:
                if ',' in section:
                    key, value = section.split(',')
                else:
                    key = value = section
                sections.append(SimpleTerm(key, key, value))
            sectionLines = sections
        return sectionLines

    @property
    def left(self):
        leftSections = self._createSectionList( getattr(self.context, 'navigation_sections_left', []))
        return leftSections

    @property
    def right(self):
        rightSections = self._createSectionList( getattr(self.context, 'navigation_sections_right', []))
        return rightSections


@indexer(Interface)
def getNavSectionsForIndex(obj, **kwargs):
    try:
        nav = INavigationSectionPosition(obj)
        return nav.section
    except (ComponentLookupError, TypeError, ValueError):
        raise AttributeError

def objectNavigationSet(obj, event):
    """ Checks if the object's navigations ection are modified. If true, catalog
        is updated. """

    for desc in event.descriptions:
        if desc.interface == INavigationSectionPosition:
            obj.reindexObject()
            break
