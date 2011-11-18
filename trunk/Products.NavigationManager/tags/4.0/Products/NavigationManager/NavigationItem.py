""" Navigation Items
"""
from Products.Archetypes import atapi
from Products.ATContentTypes.content.folder import ATFolder
from Products.CMFCore.utils import getToolByName

schema = atapi.Schema((
    atapi.StringField(
        name='url',
        widget=atapi.StringWidget(
            label='Url',
            label_msgid='NavigationManager_label_url',
            i18n_domain='NavigationManager',
        )
    ),
))

NavigationItem_schema = getattr(ATFolder, 'schema',
                                atapi.Schema(())).copy() + schema.copy()

class NavigationItem(ATFolder):
    """ Navigation Item
    """
    meta_type = archetype_name = portal_type = 'NavigationItem'
    schema = NavigationItem_schema

    def selected(self, tabselected='default', language=None):
        """ Is node selected """
        request = getattr(self, 'REQUEST', {})

        translation = (self.getTranslation(language)
                       if hasattr(self, 'getTranslation') else None)

        if language is not None and translation is not None:
            myUrl = self.getTranslation(language).getUrl()
        else:
            myUrl = self.getUrl()

        url = request.get('HTTP_REFERER', '')
        if myUrl.startswith('/'):
            url = request.get('PATH_INFO', '')

        return (self.getId() == tabselected) or (
            tabselected == 'default') and myUrl == url

    def getTree(self, local = False, tabselected='default',
                language = None, recursive=True):
        """ Returns a list  of menu items objects from the root of this
            menu manager. Useful to generate top navigation like portal tabs.
        """
        request = getattr(self, 'REQUEST', {})
        actualUrl = request.get('ACTUAL_URL', '')
        url = request.get('HTTP_REFERER', '')
        if local or not url:
            url = actualUrl
        result = []
        subItemSelected = False
        wftool = getToolByName(self, 'portal_workflow')

        for n in self.contentValues():
            # if workflow state for this navigationitem is private or draft
            # it shouldn't show up in the menu
            state = wftool.getInfoFor(n, 'review_state')
            if state != 'published':
                continue

            if recursive:
                children, selected = n.getTree(local, tabselected, language)
            else:
                children, selected = [], self.selected(tabselected, language)

            if language is not None:
                translation = (n.getTranslation(language)
                               if hasattr(n, 'getTranslation') else None)

                if translation:
                    if wftool.getInfoFor(translation,
                                         'review_state') != 'published':
                        # we have a translation but it's not published
                        # so we don't fallback here
                        continue
                    n = translation

            result.append({'item': { 'title': n.Title(),
                                     'id' : n.getId(),
                                     'description' : n.Description(),
                                     'url' : n.getUrl() },
                           'children': children,
                           'selected': selected,
                           })

            if selected:
                subItemSelected = True

        # Top menu selected if a subitem is selected
        selected = subItemSelected or self.selected(tabselected, language)
        return result, selected
