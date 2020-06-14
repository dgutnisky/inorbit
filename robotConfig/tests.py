from django.urls import resolve
from django.test import TestCase
from robotConfig.views import index

# Create your tests here.

class Index(TestCase):
    def test_root_url_resolves_to_index_view(self):
        found = resolve('/robotConfig/')
        self.assertEqual(found.func,index)
