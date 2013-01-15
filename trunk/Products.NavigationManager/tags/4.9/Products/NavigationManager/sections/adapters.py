""" Sections
"""
from persistent.dict import PersistentDict
from zope.event import notify
from zope.interface import implements
from zope.annotation.interfaces import IAnnotations
from zope.lifecycleevent import ObjectModifiedEvent, Attributes
from zope.schema.vocabulary import SimpleTerm
from Products.PloneLanguageTool.interfaces import ITranslatable
from Products.NavigationManager.config import PROJECTNAME as KEY
from Products.NavigationManager.sections.interfaces import (
    INavigationSectionPosition,
    INavigationSections,
)

class NavigationSectionPosition(object):
    """ Addapter to set / get default navigation section within annotations

    __annotations__['NavigationManager'] = {'section': None}
    """
    implements(INavigationSectionPosition)

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
        """ Getter
        """
        anno = IAnnotations(self.context)
        mapping = anno.get(KEY)
        return mapping['section']

    @section.setter
    def section(self, value):
        """ Setter
        """
        anno = IAnnotations(self.context)
        mapping = anno.get(KEY)
        mapping['section'] = value
        info = Attributes(INavigationSectionPosition, 'section')
        notify(ObjectModifiedEvent(self.context, info))

class NavigationSections(object):
    """ Navigation sections
    """
    implements(INavigationSections)

    def __init__(self, context):
        if ITranslatable.providedBy(context):
            self.context = context.getCanonical()
        else:
            self.context = context

    def _createSectionList(self, sectionLines):
        """ Create section list
        """
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
        """ Left sections
        """
        leftSections = self._createSectionList(
            getattr(self.context, 'navigation_sections_left', []))
        return leftSections

    @property
    def right(self):
        """ Right sections
        """
        rightSections = self._createSectionList(
            getattr(self.context, 'navigation_sections_right', []))
        return rightSections
