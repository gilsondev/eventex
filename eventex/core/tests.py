from django.test import TestCase


class HomeTest(TestCase):
    def setUp(self) -> None:
        self.response = self.client.get("/")

    def test_get(self):
        """GET / must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """GET / must render the index.html template"""
        self.assertTemplateUsed(self.response, "index.html")

    def test_subscription_link(self):
        self.assertContains(self.response, 'href="/inscricao/"')
