# -*- coding: utf-8 -*-

from plone import api
from plone.app.uuid.utils import uuidToObject
from plone.tiles import Tile
from Products.CMFCore import permissions
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


class SearchPubblicazioni(Tile):
    """
    Tile for pubblicazioni search on site
    """

    def get_search_path(self):
        # search_path = self.data.get('path', '')
        obj = uuidToObject(self.data.get('search_path', ''))
        if obj:
            path = '/'.join(obj.getPhysicalPath())
            return path
        else:
            return ""

    def get_authors(self):
        search_path = self.get_search_path()
        portal_catalog = api.portal.get_tool('portal_catalog')
        # api.user.has_permission(permissions.ModifyPortalContent, obj=self.context)  # noqa
        # CHECK: va bene fare solo la separazione per gli anonimi o meglio
        # scremare anche per permessi?
        if api.user.is_anonymous():
            # mostriamo solo le voci degli autori dei contenuti pubblicati
            results = portal_catalog(
                portal_type='Pubblicazione',
                path=search_path,
                review_state='published')
        else:
            results = portal_catalog(
                portal_type='Pubblicazione',
                path=search_path)

        authors_options = []

        for brain in results:
            if brain.authors:
                for author in brain.authors:
                    authors_options.append(author)

        terms = [SimpleVocabulary.createTerm(author, author, author) for author in set(authors_options)]  # noqa
        vocabulary = SimpleVocabulary(terms)

        # Vecchio funzionamento, dove venivamo mostrati tutti gli autori
        # factory = getUtility(
        #     IVocabularyFactory,
        #     'rer.pubblicazioni.used_authors')
        # vocabulary = factory(self.context)

        return vocabulary

    def get_publication_type(self):
        values = api.portal.get_registry_record('rer.pubblicazioni.browser.settings.IRerPubblicazioniSettings.tipologie')  # noqa
        if values:
            return values.split('\r\n')
        else:
            return []

    def get_publication_language(self):
        values = api.portal.get_registry_record('rer.pubblicazioni.browser.settings.IRerPubblicazioniSettings.lingue')  # noqa
        if values:
            return values.split('\r\n')
        else:
            return []
