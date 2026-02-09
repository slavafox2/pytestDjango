from unittest.mock import patch
import json

from django.core import mail
from django.test import TestCase, Client


class EmailUnittest(TestCase):
    def test_send_email_should_have_success(self) -> None:
        with self.settings(
            EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"
        ):
            self.assertEqual(len(mail.outbox), 0)
            # Send message
            mail.send_mail(
                subject="Test Subject here",
                message="Test is the Message here",
                from_email="testemail@yandex.by",
                recipient_list=["testemail@yandex.by"],
                fail_silently=False,
            )

            # Test that one message has been sent
            self.assertEqual(mail.outbox[0].subject, "Test Subject here")

    def test_send_email_without_arguments_should_send_empty_email(self) -> None:
        client = Client()
        with patch(
                "companies.views.send_mail"
        ) as mocked_send_mail_function:
            response = client.post(path="/send-email")
            response_content = json.loads(response.content)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_content["status"], "success")
            self.assertEqual(response_content["info"], "email sent successfully")
            mocked_send_mail_function.assert_called_with(
                subject=None,
                message=None,
                from_email="rteyti334@yandex.by",
                recipient_list=["rteyti334@yandex.by"],
            )

    def test_send_email_with_get_verb_should_fail(self) -> None:
        client = Client()
        response = client.get(path="/send-email")
        assert response.status_code == 405
        assert json.loads(response.content) == {"detail": "Method \"GET\" not allowed."}
