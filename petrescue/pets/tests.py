from datetime import date

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from .models import PetReport, Claim


class PetReportModelTests(TestCase):
    def test_create_report(self):
        report = PetReport.objects.create(
            species="dog",
            color="brown",
            location_found="Park",
            date_found=date.today(),
            contact_email="owner@example.com",
        )
        self.assertEqual(report.status, "found")
        self.assertEqual(str(report).startswith("Dog"), True)


class ClaimFlowTests(TestCase):
    def setUp(self):
        self.report = PetReport.objects.create(
            species="cat",
            color="black",
            location_found="Main St",
            date_found=date.today(),
            contact_email="reporter@example.com",
        )

    def test_claim_submission_sends_email(self):
        self.assertEqual(len(mail.outbox), 0)
        claim = Claim.objects.create(
            pet=self.report,
            claimer_name="Alice",
            claimer_email="alice@example.com",
            message="This might be my cat",
        )
        self.assertEqual(claim.status, "pending")
        self.assertGreaterEqual(len(mail.outbox), 1)

    def test_claim_status_update_marks_report_claimed_and_emails(self):
        claim = Claim.objects.create(
            pet=self.report,
            claimer_name="Bob",
            claimer_email="bob@example.com",
        )
        mail.outbox.clear()
        claim.status = "approved"
        claim.save()
        self.report.refresh_from_db()
        self.assertEqual(self.report.status, "claimed")
        self.assertGreaterEqual(len(mail.outbox), 1)


class ViewsTests(TestCase):
    def setUp(self):
        self.report = PetReport.objects.create(
            species="dog",
            color="white",
            location_found="River",
            date_found=date.today(),
        )

    def test_list_view(self):
        url = reverse("pets:report_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Found Pets")

    def test_create_view(self):
        url = reverse("pets:report_create")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_detail_and_claim(self):
        detail = reverse("pets:report_detail", args=[self.report.pk])
        self.assertEqual(self.client.get(detail).status_code, 200)
        claim_url = reverse("pets:claim_create", args=[self.report.pk])
        resp = self.client.post(
            claim_url,
            {
                "claimer_name": "Zed",
                "claimer_email": "zed@example.com",
                "message": "Mine",
            },
        )
        self.assertEqual(resp.status_code, 302)
