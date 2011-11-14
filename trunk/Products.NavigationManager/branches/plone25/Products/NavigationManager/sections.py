from zope.interface import Interface, Attribute, implements
from zope.component import adapts
from zope.component.exceptions import ComponentLookupError
from zope.app.annotation.interfaces import IAnnotations
#from zope.app.component.hooks import getSite
from zope.app.event.objectevent import ObjectModifiedEvent, Attributes
#from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm #, SimpleVocabulary
from zope.event import notify
import logging
logger = logging.getLogger("Products.NavigationManager.sections")
ITranslatable = None
try:
    from Products.LinguaPlone.interfaces import ITranslatable
except ImportError, err:
    logger.info(err)
    
from persistent.dict import PersistentDict

#from Products.CMFCore.utils import getToolByName

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

    #def section():
    def gets(self):
        anno = IAnnotations(self.context)
        mapping = anno.get(KEY)
        return mapping['section']
    def sets(self, value):
        anno = IAnnotations(self.context)
        mapping = anno.get(KEY)
        mapping['section'] = value
        info = Attributes(INavigationSectionPosition, 'section')
        notify(ObjectModifiedEvent(self.context, info))
    #return property(get, set)
    section = property(gets, sets)


class NavigationSections(object):
    implements(INavigationSections)
    adapts(Interface)
    
    def __init__(self, context):
        if ITranslatable is not None and ITranslatable.providedBy(context):
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


def getNavSectionsForIndex(obj, portal, **kwargs):
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
