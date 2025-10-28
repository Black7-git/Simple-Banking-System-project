from django.test import TestCase
from django.urls import reverse
from .models import PetReport, ReportType, PetSpecies
from datetime import date


class PetReportTests(TestCase):
    def test_create_report_and_detail(self):
        r = PetReport.objects.create(
            report_type=ReportType.FOUND,
            species=PetSpecies.DOG,
            breed="Labrador",
            color="Black",
            distinctive_marks="White patch",
            location="Central Park",
            date_seen=date.today(),
            description="Friendly dog",
            reporter_name="Alex",
            reporter_email="alex@example.com",
        )
        self.assertTrue(r.reference_code)
        url = reverse("pets:report_detail", args=[r.reference_code])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, r.reference_code)

    def test_search_reports(self):
        PetReport.objects.create(
            report_type=ReportType.LOST,
            species=PetSpecies.CAT,
            location="Downtown",
            date_seen=date.today(),
            reporter_name="Sam",
            reporter_email="sam@example.com",
        )
        resp = self.client.get(reverse("pets:search"), {"q": "Downtown"})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Downtown")

    def test_create_report_form(self):
        resp = self.client.get(reverse("pets:report_create"))
        self.assertEqual(resp.status_code, 200)
        data = {
            "report_type": ReportType.LOST,
            "species": PetSpecies.BIRD,
            "breed": "",
            "color": "Yellow",
            "distinctive_marks": "",
            "location": "Riverside",
            "date_seen": date.today(),
            "description": "",
            "reporter_name": "Jane",
            "reporter_email": "jane@example.com",
            "reporter_phone": "",
        }
        resp = self.client.post(reverse("pets:report_create"), data)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/report/", resp["Location"])