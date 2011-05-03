""" Testing environment
"""
from Products.PloneTestCase import PloneTestCase

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.GenericSetup import EXTENSION, profile_registry

PloneTestCase.installProduct('NavigationManager')

@onsetup
def setup_navigationmanager():
    """ Setup Products.NavigationManager
    """
    fiveconfigure.debug_mode = True
    from Products import NavigationManager
    zcml.load_config('configure.zcml', NavigationManager)
    zcml.load_config('testing.zcml', NavigationManager.tests)
    fiveconfigure.debug_mode = False

setup_navigationmanager()
PloneTestCase.setupPloneSite(extension_profiles = [
    'NavigationManager:default',
    'NavigationManager:testfixture'
])

class NavigationManagerTestCase(PloneTestCase.PloneTestCase):
    """Base TestCase for NavigationManager."""
