
from django.test import TestCase, LiveServerTestCase


# Create your tests here.
class CITest(TestCase):
    def test_sanity(self):
        self.assertTrue(True)


class CDBuildTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Ensure the test server loads static files
        #call_command('collectstatic', verbosity=0, interactive=False)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_css_delivery(self):
        response = self.client.get('/static/css/style.css')
        self.assertEqual(response.status_code, 200)
