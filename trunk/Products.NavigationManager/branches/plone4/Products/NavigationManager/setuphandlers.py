from Products.CMFCore.utils import getToolByName

def setupVarious(context):
    # only run this step if we are in NavigationManager profile
    # learned from Aspelis book, Professional Plone Development
    if context.readDataFile('products.navigationmanager.txt') is None:
        return

    #site = context.getSite()
    logger = context.getLogger('navigationamnager')

    setupCatalog(context)
    logger.info("navigationmanager_various: navSection index is a method")


def setupCatalog(context):
    site = context.getSite()
    catalog = getToolByName(site, 'portal_catalog')
    catalog.manage_reindexIndex(ids=['navSection', 'is_default_page'])

    # if is_empty index isn't updated yet, update the whole catalog
    empty = len(catalog.searchResults(is_empty=False))
    non_empty = len(catalog.searchResults(is_empty=True))
    total = len(catalog.searchResults())
    if empty + non_empty < total/2:
        catalog.refreshCatalog()
