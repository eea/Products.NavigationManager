""" Sections
"""
from Products.NavigationManager.sections.interfaces import INavigationSections
from Products.Five.browser import BrowserView

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
