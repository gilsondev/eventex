from django.core import mail
from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):
    def setUp(self):
        self.response = self.client.get("/inscricao/")

    def test_get(self):
        """GET /inscricao/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.response, "subscriptions/subscription_form.html")

    def test_html(self):
        """Must html contain input tags"""
        self.assertContains(self.response, "<form")
        self.assertContains(self.response, "<input", 6)
        self.assertContains(self.response, 'type="text', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """HTML must contain csrf_token"""
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_form(self):
        """Context must have subscription form"""
        form = self.response.context["form"]
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = self.response.context["form"]
        self.assertSequenceEqual(["name", "cpf", "email", "phone"], list(form.fields))


class SubscriptionPostTest(TestCase):
    def setUp(self):
        data = dict(
            name="Carlos Silva", cpf="12345678901", email="carlos.silva@mail.com", phone="61 99876-1018"
        )
        self.response = self.client.post("/inscricao/", data)

    def test_post(self):
        """Valid POST should redirect to /inscricao/"""

        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_mail_subject(self):
        email = mail.outbox[0]
        expect = "Confirmação de inscrição"
        self.assertEqual(expect, email.subject)

    def test_subscription_mail_from(self):
        email = mail.outbox[0]
        expect = "contato@eventex.com.br"
        self.assertEqual(expect, email.from_email)

    def test_subscription_mail_to(self):
        email = mail.outbox[0]
        expect = ["contato@eventex.com.br", "carlos.silva@mail.com"]
        self.assertEqual(expect, email.to)

    def test_subscription_mail_body(self):
        email = mail.outbox[0]

        self.assertIn("Carlos Silva", email.body)
        self.assertIn("12345678901", email.body)
        self.assertIn("carlos.silva@mail.com", email.body)
        self.assertIn("61 99876-1018", email.body)


class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.response = self.client.post("/inscricao/", {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, "subscriptions/subscription_form.html")

    def test_has_form(self):
        form = self.response.context["form"]
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.response.context["form"]
        self.assertTrue(form.errors)


class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(
            name="Carlos Silva", cpf="12345678901", email="carlos.silva@mail.com", phone="61 99876-1018"
        )
        response = self.client.post("/inscricao/", data, follow=True)
        self.assertContains(response, "Inscrição realizada com sucesso")
