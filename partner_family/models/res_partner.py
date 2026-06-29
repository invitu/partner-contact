# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_family = fields.Boolean(default=False)

    company_type = fields.Selection(
        selection_add=[("family", "Family")],
        ondelete={"family": "set default"},
        default="company",
    )

    @api.depends("is_company", "is_family")
    def _compute_company_type(self):
        for partner in self:
            if partner.is_family:
                partner.company_type = "family"
            else:
                partner.company_type = "company" if partner.is_company else "person"

    def _write_company_type(self):
        for partner in self:
            if partner.company_type == "family":
                partner.is_family = True
                partner.is_company = True
            elif partner.company_type == "company":
                partner.is_family = False
                partner.is_company = True
            else:
                partner.is_family = False
                partner.is_company = False

    @api.onchange("company_type")
    def onchange_company_type(self):
        if self.company_type == "family":
            self.is_company = True
            self.is_family = True
        else:
            res = super().onchange_company_type()
            self.is_family = False
            return res

    def get_family(self):
        """Return the family partner linked to this partner."""
        self.ensure_one()
        if self.is_family:
            return self
        if self.parent_id and self.parent_id.is_family:
            return self.parent_id
        return self.browse()

    def get_family_members(self):
        """Return all members of the family."""
        self.ensure_one()
        family = self.get_family()
        if not family:
            return self.browse()
        return family.child_ids
