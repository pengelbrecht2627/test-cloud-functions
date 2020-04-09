from .email import Attachment, Email, Mail, SGAttachment


class TestAttachment:
    def test_conversion_to_sendgrid_attachment(self):
        """Test converion to a SendGrid attachment
        """

        lAttachment = Attachment(
            content=b"1234", mime_type="fake/text", name="attachment.fake"
        )

        assert lAttachment.to_sendgrid_attachment().get() == {
            "content": "MTIzNA==",
            "filename": "attachment.fake",
            "type": "fake/text",
            "disposition": "attachment",
        }


class TestEmail_to_sendgrid_email:
    def test_missing_optionals(self):
        """Test to still convert when optionals are missing
        """

        lEmail = Email(
            subject="Email subject",
            html="<p>Hello</p>",
            plain_text="Hello",
            from_email="from@domain.com",
            to=["rec1@domain.com", "smart <rec2@yahoo.com>"],
        )

        assert lEmail.to_sendgrid_email().get() == {
            "from": {"email": "from@domain.com"},
            "subject": "Email subject",
            "content": [
                {"type": "text/plain", "value": "Hello"},
                {"type": "text/html", "value": "<p>Hello</p>"},
            ],
            "personalizations": [
                {
                    "to": [
                        {"email": "rec1@domain.com"},
                        {"email": "rec2@yahoo.com", "name": "smart"},
                    ]
                }
            ],
        }

    def test_with_one_category(self):
        """Test that a single category is added correctly
        """

        lEmail = Email(
            subject="subject",
            html="html",
            plain_text="plain",
            from_email="from@d.com",
            to=["rec1@domain.com"],
            categories=["cat"],
        )

        assert lEmail.to_sendgrid_email().get() == {
            "from": {"email": "from@d.com"},
            "subject": "subject",
            "content": [
                {"type": "text/plain", "value": "plain"},
                {"type": "text/html", "value": "html"},
            ],
            "personalizations": [{"to": [{"email": "rec1@domain.com"}]}],
            "categories": ["cat"],
        }

    def test_with_multiple_categories(self):
        """Test that multiple categories are added correctly
        """

        lEmail = Email(
            subject="subject",
            html="html",
            plain_text="plain",
            from_email="me <from@d.com>",
            to=["rec1@domain.com"],
            categories=["cat1", "cat2", "cat3", "cat4"],
        )

        assert lEmail.to_sendgrid_email().get() == {
            "from": {"email": "from@d.com", "name": "me"},
            "subject": "subject",
            "content": [
                {"type": "text/plain", "value": "plain"},
                {"type": "text/html", "value": "html"},
            ],
            "personalizations": [{"to": [{"email": "rec1@domain.com"}]}],
            "categories": ["cat4", "cat3", "cat2", "cat1"],
        }

    def test_with_attachment(self):
        """Test that a single attachment is added correctly
        """

        lEmail = Email(
            subject="subject",
            html="html",
            plain_text="plain",
            from_email="from@d.com",
            to=["rec1@domain.com"],
            attachment=Attachment(
                content=b"test", mime_type="text/fake", name="name.fake"
            ),
        )

        assert lEmail.to_sendgrid_email().get() == {
            "from": {"email": "from@d.com"},
            "subject": "subject",
            "content": [
                {"type": "text/plain", "value": "plain"},
                {"type": "text/html", "value": "html"},
            ],
            "personalizations": [{"to": [{"email": "rec1@domain.com"}]}],
            "attachments": [
                {
                    "type": "text/fake",
                    "content": "dGVzdA==",
                    "filename": "name.fake",
                    "disposition": "attachment",
                },
            ],
        }