""" Various setups
"""
def setupVarious(context):
    """ Custom setup """

    if context.readDataFile('products.navigationmanager.txt') is None:
        return
