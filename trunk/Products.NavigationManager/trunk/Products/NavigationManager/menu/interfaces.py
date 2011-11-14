""" Menu interfaces
"""

from zope.app.publisher.interfaces.browser import IBrowserSubMenuItem
from zope.app.publisher.interfaces.browser import IBrowserMenu

class INavigationSubMenuItem(IBrowserSubMenuItem):
    """The menu item linking to the "Navigation" menu.
    """

class INavigationMenu(IBrowserMenu):
    """The navigation menu.

    This gets its menu items from portal_actions.
    """
