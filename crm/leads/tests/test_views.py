from django.shortcuts import reverse
from django.test import TestCase


class LandingPageTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse("landing-page"))
        self.assertEqual(response.status.code, 200)
        self.assertTemplateUsed(response, "landing.html")
