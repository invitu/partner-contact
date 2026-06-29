# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestPartnerFamily(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.family = cls.env["res.partner"].create(
            {
                "name": "Family Dupont",
                "company_type": "family",
            }
        )
        cls.member1 = cls.env["res.partner"].create(
            {
                "name": "Jean Dupont",
                "parent_id": cls.family.id,
            }
        )
        cls.member2 = cls.env["res.partner"].create(
            {
                "name": "Marie Dupont",
                "parent_id": cls.family.id,
            }
        )
        cls.standalone = cls.env["res.partner"].create(
            {
                "name": "Standalone Partner",
            }
        )

    def test_company_type_family(self):
        """Setting company_type='family' sets is_family=True and is_company=True."""
        self.assertEqual(self.family.company_type, "family")
        self.assertTrue(self.family.is_family)
        self.assertTrue(self.family.is_company)

    def test_company_type_company(self):
        """Setting company_type='company' clears is_family."""
        partner = self.env["res.partner"].create(
            {
                "name": "Test Company",
                "company_type": "company",
            }
        )
        self.assertFalse(partner.is_family)
        self.assertTrue(partner.is_company)

    def test_company_type_person(self):
        """Setting company_type='person' clears is_family and is_company."""
        self.assertFalse(self.standalone.is_family)
        self.assertFalse(self.standalone.is_company)
        self.assertEqual(self.standalone.company_type, "person")

    def test_is_family_flag_sets_company_type(self):
        """Setting is_family=True computes company_type='family'."""
        partner = self.env["res.partner"].create({"name": "Test"})
        partner.is_family = True
        self.assertEqual(partner.company_type, "family")

    def test_get_family_from_family_partner(self):
        """get_family() on a family partner returns itself."""
        self.assertEqual(self.family.get_family(), self.family)

    def test_get_family_from_member(self):
        """get_family() on a member returns the family partner."""
        self.assertEqual(self.member1.get_family(), self.family)

    def test_get_family_no_family(self):
        """get_family() on a standalone partner returns empty recordset."""
        self.assertFalse(self.standalone.get_family())

    def test_get_family_members(self):
        """get_family_members() returns all child_ids of the family."""
        members = self.family.get_family_members()
        self.assertIn(self.member1, members)
        self.assertIn(self.member2, members)

    def test_get_family_members_from_member(self):
        """get_family_members() works from a member too."""
        members = self.member1.get_family_members()
        self.assertIn(self.member2, members)

    def test_get_family_members_no_family(self):
        """get_family_members() returns empty recordset for standalone."""
        self.assertFalse(self.standalone.get_family_members())

    def test_family_no_address_required(self):
        """A family partner can be created without an address."""
        family = self.env["res.partner"].create(
            {
                "name": "No Address Family",
                "company_type": "family",
            }
        )
        self.assertTrue(family.is_family)
        self.assertFalse(family.street)
