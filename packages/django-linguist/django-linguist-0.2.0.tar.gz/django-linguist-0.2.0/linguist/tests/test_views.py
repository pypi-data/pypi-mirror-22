# -*- coding: utf-8 -*-
import json

from django.utils import translation

from exam.decorators import before

from .base import BaseTestCase
from .models import FooModel


class ViewTest(BaseTestCase):
    """
    Tests Linguist views.
    """

    @before
    def setup(self):
        obj = self.translated_instance # noqa

    def _check_language(self, response):
        lang = translation.get_language()
        self.assertEqual(response.status_code, 200)
        dct = json.loads(response.content.decode('utf-8') )
        self.assertEqual(dct['title'], lang)

    def test_translation_activate(self):
        for language in self.languages:
            translation.activate(language)
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self._check_language(response)

    def test_set_lang(self):
        for language in self.languages:
            response = self.client.post('/i18n/setlang/', {'language': language}, follow=True)
            self.assertEqual(response.status_code, 200)
            self._check_language(response)
