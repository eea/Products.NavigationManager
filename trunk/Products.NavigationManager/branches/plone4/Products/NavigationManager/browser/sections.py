""" Sections
"""
from zope.event import notify
from zope.interface import implements
from zope.component import queryAdapter
from zope.lifecycleevent import ObjectModifiedEvent, Attributes

from Products.NavigationManager.sections import (
    INavigationSectionPosition,
    INavigationSections,
)
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Acquisition import aq_base
from Products.NavigationManager.browser.interfaces import (
    IContentNavigationSectionMenu,
)


class SetNavigationSection(BrowserView):
    """ sets navigation section for current object. """

    def __call__(self):
        section = self.request.get('section', None)
        if section == 'exclude':
            self.context.setExcludeFromNav(True)
        elif section == 'reset':
            self.context.setExcludeFromNav(False)
            navContext = INavigationSectionPosition(self.context)
            navContext.section = None
        elif section is not None:
            navContext = INavigationSectionPosition(self.context)
            navContext.section = section
        info = Attributes(INavigationSectionPosition, 'section')
        notify(ObjectModifiedEvent(self.context, info))

        url = self.request.get('HTTP_REFERER', None)
        if url is None:
            url = self.context.absolute_url()
        return self.request.RESPONSE.redirect(url)

class SectionsForContentNavigationMenu(BrowserView):
    """ return the menu for navigation sections in content views. """
    implements(IContentNavigationSectionMenu)

    def __init__(self, context, request):
        self.navContext = queryAdapter(context, INavigationSectionPosition)
        self.context = context
        self.request = request

    def display(self):
        """ Display
        """
        if self.navContext is None:
            return False
        mship = getToolByName(self.context, 'portal_membership')
        return mship.checkPermission('Modify portal content', self.context)

    @property
    def menu(self):
        """ Menu
        """
        navContext = self.navContext
        if not self.display():
            return []

        context = self.context
        sections = INavigationSections(context)
        currentSection = navContext.section
        if hasattr(aq_base(context), 'exclude_from_nav'):
            exclude_from_nav = context.exclude_from_nav()
        else:
            exclude_from_nav = False
        menu = [ { 'id' : 'reset',
                   'title' : 'Reset',
                   'current' : False },
                 { 'id' : 'exclude',
                   'title' : 'Exclude',
                   'current' : exclude_from_nav } ]

        if sections.left:
            menu.append( { 'id' : 'separator',
                           'title' : 'Left sections',
                           'current' : False })
        for section in sections.left:
            menu.append( { 'id': section.value,
                           'title' : section.title,
                           'current' : currentSection == section.value })

        if sections.right:
            menu.append( { 'id' : 'separator',
                           'title' : 'Right sections',
                           'current' : False })
        for section in sections.right:
            menu.append( { 'id': section.value,
                           'title' : section.title,
                           'current' : currentSection == section.value  })
        return menu



class GetNavigationSection(BrowserView):
    """ Gets navigation section for current object. """

    def __call__(self):
        navContext = INavigationSectionPosition(self.context)
        return  navContext.section

class LeftNavigationSectionPortlet(BrowserView):
    """ Gets navigation section for current object. """

    def __call__(self):
        context = self.context
        sections = INavigationSections(context)
        rendered = ''
        for section in sections.left:
            template = context.unrestrictedTraverse(
                'portlet_navigation_sections')

            rendered += template(
                section=section.value, sectionTitle=section.title)
        return rendered


class RightNavigationSectionPortlet(BrowserView):
    """ Gets navigation section for current object. """

    def __call__(self):
        context = self.context
        sections = INavigationSections(context)
        rendered = ''
        for section in sections.right:
            template = context.unrestrictedTraverse(
                'portlet_navigation_sections')

            rendered += template(
                section=section.value, sectionTitle=section.title)
        return rendered
