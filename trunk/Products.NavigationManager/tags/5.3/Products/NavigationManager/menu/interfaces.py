""" Menu interfaces
"""

from zope.browsermenu.interfaces import IBrowserSubMenuItem
from zope.browsermenu.interfaces import IBrowserMenu

class INavigationSubMenuItem(IBrowserSubMenuItem):
    """The menu item linking to the "Navigation" menu.
    """

class INavigationMenu(IBrowserMenu):
    """The navigation menu.

    This gets its menu items from portal_actions.
    """
