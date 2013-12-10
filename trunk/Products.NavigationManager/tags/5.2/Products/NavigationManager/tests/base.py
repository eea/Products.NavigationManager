""" Testing environment
"""
from Products.PloneTestCase import PloneTestCase

from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml
from Products.Five import fiveconfigure

PloneTestCase.installProduct('NavigationManager')

@onsetup
def setup_navigationmanager():
    """ Setup Products.NavigationManager
    """
    fiveconfigure.debug_mode = True
    from Products import NavigationManager
    zcml.load_config('configure.zcml', NavigationManager)
    fiveconfigure.debug_mode = False

setup_navigationmanager()
PloneTestCase.setupPloneSite(extension_profiles = [
    'Products.NavigationManager:default',
])

class NavigationManagerTestCase(PloneTestCase.PloneTestCase):
    """Base TestCase for NavigationManager."""
