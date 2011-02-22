from Products.CMFCore.utils import getToolByName
from Products.NavigationManager.catalog import reindexTree

def reindexIsEmptyForSite(context, query):
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog(query)

    brainsByURL = {}
    for b in brains:
        brainsByURL[b.getURL()] = b

    urls = [ b.getURL() for b in brains ]
    urls.sort()
    
    deepest = []
    url = urls.pop()
    while urls:
        next = urls.pop()
        if next not in url:
            deepest.append(next)
            url = next
    deepest.append(url)
    

    for u in deepest:
        reindexTree(brainsByURL[u].getObject())

                                       
