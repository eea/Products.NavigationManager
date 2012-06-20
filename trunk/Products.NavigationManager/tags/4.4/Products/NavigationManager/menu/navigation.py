""" Navigation Menu
"""
from zope.event import notify
from zope.interface import implements
from zope.component import getMultiAdapter, queryAdapter
from zope.lifecycleevent import ObjectModifiedEvent, Attributes
from zope.app.publisher.browser.menu import BrowserMenu
from zope.app.publisher.browser.menu import BrowserSubMenuItem
from plone.app.contentmenu import PloneMessageFactory as _

from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.NavigationManager.menu.interfaces import INavigationMenu
from Products.NavigationManager.menu.interfaces import INavigationSubMenuItem
from Products.NavigationManager.sections.interfaces import (
    INavigationSections,
    INavigationSectionPosition,
)

class NavigationMenu(BrowserSubMenuItem):
    """ Navigation submenu item
    """
    implements(INavigationSubMenuItem)

    title = _(u'label_navigation_menu', default=u'Navigation')
    description = _(u'title_navigation_menu', default=u'Navigation actions')
    submenuId = 'eea_navigation'

    order = 5
    extra = {'id': 'eea-navigation'}

    @property
    def context_state(self):
        """ State
        """
        return getMultiAdapter((self.context, self.request),
                               name=u'plone_context_state')

    @property
    def action(self):
        """ Submenu action
        """
        return self.context.absolute_url()

    def available(self):
        """ Is this menu available?
        """
        navContext = queryAdapter(self.context, INavigationSectionPosition)
        if navContext is None:
            return False
        mship = getToolByName(self.context, 'portal_membership')
        return mship.checkPermission('Modify portal content', self.context)

    def selected(self):
        """ Is this item selected?
        """
        return False

class NavigationMenuItems(BrowserMenu):
    """ Navigation menu
    """
    implements(INavigationMenu)

    def getMenuItems(self, context, request):
        """ Return menu items
        """
        url = context.absolute_url()
        action = url + '/@@setNavigationSection?section=%s'
        exclude = (bool(context.exclude_from_nav())
                   if hasattr(context, 'exclude_from_nav') else False)

        menu = [
            {
                'title': 'Reset',
                'description': '',
                'action': action % 'reset',
                'selected': False,
                'icon': None,
                'extra': {'id': 'reset', 'separator': None, 'class': ''},
                'submenu': None,
            },
            {
                'title': 'Exclude',
                'description': '',
                'action': action % 'exclude',
                'selected': exclude,
                'icon': None,
                'extra': {
                    'id': 'exclude',
                    'separator': None,
                    'class': 'actionMenuSelected' if exclude else '',
                    },
                'submenu': None,
            },
        ]

        sections = queryAdapter(context, INavigationSections)
        if not sections:
            return menu

        #
        # Default (current) section
        #
        navContext = queryAdapter(context, INavigationSectionPosition)
        if navContext:
            current = navContext.section
        else:
            current = ''
        #
        # Left sections
        #
        left = []
        for section in sections.left:
            selected = (section.value == current)
            left.append({
                'title': section.title,
                'description': '',
                'action': action % section.value,
                'selected': selected,
                'icon': None,
                'extra': {
                    'id': section.value,
                    'separator': 'actionSeparator',
                    'class': 'actionMenuContent' + (
                        ' actionMenuSelected' if selected else ''),
                    },
                'submenu': None,
            })

        if left:
            menu.append({
                'title': 'Left sections',
                'description': '',
                'action': None,
                'selected': False,
                'icon': None,
                'extra': {
                    'id': 'left-sections',
                    'separator': 'actionSeparator',
                    'class': '',
                    },
                'submenu': None,
                })
            menu.extend(left)

        # Right sections
        right = []
        for section in sections.right:
            selected = (section.value == current)
            right.append({
                'title': section.title,
                'description': '',
                'action': action % section.value,
                'selected': selected,
                'icon': None,
                'extra': {
                    'id': section.value,
                    'separator': None,
                    'class': 'actionMenuContent' + (
                        ' actionMenuSelected' if selected else ''),
                    },
                'submenu': None,
            })

        if right:
            menu.append({
                'title': 'Right sections',
                'description': '',
                'action': None,
                'selected': False,
                'icon': None,
                'extra': {
                    'id': 'right-sections',
                    'separator': 'actionSeparator',
                    'class': '',
                    },
                'submenu': None,
            })
            menu.extend(right)

        # Manage sections
        if getSecurityManager().getUser().has_role('Manager'):
            menu.append({
                'title': 'Manage sections',
                'description': '',
                'action': '%s/manage_propertiesForm' % context.absolute_url(),
                'selected': False,
                'icon': None,
                'extra': {
                    'id': 'manage-sections',
                    'separator': 'actionSeparator',
                    'class': '',
                    },
                'submenu': None,
            })

        return menu

class SetNavigationSection(BrowserView):
    """ Sets navigation section for current object.
    """
    def __call__(self):
        section = self.request.get('section', None)
        if section == 'exclude':
            if not self.context.exclude_from_nav():
                self.context.setExcludeFromNav(True)
            else:
                self.context.setExcludeFromNav(False)
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
