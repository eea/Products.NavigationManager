## Script (Python) "selectViewTemplate"
##title=Helper method to select a view template
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=templateId
status = context.portal_navigationmanager.selectViewTemplate(context, templateId)
state.set(status=status)
return state
