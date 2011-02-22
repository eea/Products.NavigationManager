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

    
def createMenuStructure(current, children, positions=[]):

    for id, menuItem in children.items():
        subMenu = getattr(aq_base(current), id, None)

        if subMenu is None:
            print "adding non-existing menu with id = " + id
            current.invokeFactory('NavigationItem',
                                         id = id,
                                         url = menuItem['url'],
                                         title = menuItem['title'])
            subMenu = getattr(current, id, None)
            
        if menuItem['children']:
            print "create children for menu id = " + id
            createMenuStructure(subMenu, menuItem['children'], menuItem['positions'] )
           

    # positions all the children according to positions list.

    if current.getId() != 'portal_navigationmanager' and current != None and positions != []:
        for id, menuItem in children.items():
          #move object as they are sorted in original position
            try:
                print id + " - setting position to " + str(positions.index(id))
                position = positions.index(id)
                current.moveObject(id, position)
                subMenu = getattr(current, id, None)
                subMenu.reindexObject()
            except:
                print "ERROR: could not move object with id=" + id


