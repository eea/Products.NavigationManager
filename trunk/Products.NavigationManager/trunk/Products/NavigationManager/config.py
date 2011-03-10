""" Config
"""
from Products.CMFCore.permissions import setDefaultRoles

PROJECTNAME = "NavigationManager"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# You can overwrite these two in an AppConfig.py:
# STYLESHEETS = [{'id': 'my_global_stylesheet.css'},
#                {'id': 'my_contenttype.css',
#              'expression': 'python:object.getTypeInfo().getId() == "MyType"'}]
# You can do the same with JAVASCRIPTS.
STYLESHEETS = []
JAVASCRIPTS = []
