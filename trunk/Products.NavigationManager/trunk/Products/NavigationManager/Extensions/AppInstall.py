from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.NavigationManager import menuConfig

def install(self):
    pass

def uninstall(self):
    pass


def createDefaultMenu(self):
    menu = menuConfig.menu
    site_positions = menuConfig.site_positions
    nav = getToolByName(self, 'portal_navigationmanager', None)
    
    createMenuStructure( nav, menu, site_positions)

    
def createMenuStructure(current, children, positions = None):
    if positions is None:
        positions = []

    for cid, menuItem in children.items():
        subMenu = getattr(aq_base(current), cid, None)

        if subMenu is None:
            print "adding non-existing menu with id = " + cid
            current.invokeFactory('NavigationItem',
                                         id = cid,
                                         url = menuItem['url'],
                                         title = menuItem['title'])
            subMenu = getattr(current, cid, None)
            
        if menuItem['children']:
            print "create children for menu id = " + cid
            createMenuStructure(subMenu, menuItem['children'], menuItem['positions'] )
           

    # positions all the children according to positions list.

    if current.getId() != 'portal_navigationmanager' and current != None and positions != []:
        for cid, menuItem in children.items():
          #move object as they are sorted in original position
            try:
                print cid + " - setting position to " + str(positions.index(cid))
                position = positions.index(cid)
                current.moveObject(cid, position)
                subMenu = getattr(current, cid, None)
                subMenu.reindexObject()
            except Exception:
                print "ERROR: could not move object with id=" + cid


