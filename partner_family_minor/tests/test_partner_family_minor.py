# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import date

from odoo.tests.common import TransactionCase


class TestPartnerFamilyMinor(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.minor_age_limit = 18
        today = date.today()
        cls.minor = cls.env["res.partner"].create(
            {
                "name": "Minor Child",
                "birthdate_date": date(today.year - 10, today.month, today.day),
            }
        )
        cls.adult = cls.env["res.partner"].create(
            {
                "name": "Adult Partner",
                "birthdate_date": date(today.year - 25, today.month, today.day),
            }
        )
        cls.no_birthdate = cls.env["res.partner"].create(
            {
                "name": "No Birthdate",
            }
        )
        cls.borderline = cls.env["res.partner"].create(
            {
                "name": "Exactly 18",
                "birthdate_date": date(today.year - 18, today.month, today.day),
            }
        )

    def test_minor_is_minor(self):
        """Partner aged 10 is a minor."""
        self.assertTrue(self.minor.is_minor)

    def test_adult_not_minor(self):
        """Partner aged 25 is not a minor."""
        self.assertFalse(self.adult.is_minor)

    def test_exactly_age_limit_not_minor(self):
        """Partner exactly at the age limit is not a minor."""
        self.assertFalse(self.borderline.is_minor)

    def test_no_birthdate_not_minor(self):
        """Partner without birthdate is not considered a minor."""
        self.assertFalse(self.no_birthdate.is_minor)

    def test_custom_age_limit(self):
        """Changing minor_age_limit recomputes is_minor."""
        self.env.company.minor_age_limit = 30
        self.adult._compute_is_minor()
        self.assertTrue(self.adult.is_minor)
        self.env.company.minor_age_limit = 18
        self.adult._compute_is_minor()
        self.assertFalse(self.adult.is_minor)
