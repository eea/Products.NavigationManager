## Script (Python) "selectDefaultPage"
##title=Helper method to select a default page for a folder view
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=objectId=None

status = context.portal_navigationmanager.saveDefaultPage(context, objectId)
state.set(status=status)
return state
