# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_minor = fields.Boolean(
        compute="_compute_is_minor",
        store=True,
    )

    @api.depends("age", "company_id.minor_age_limit")
    def _compute_is_minor(self):
        for partner in self:
            limit = partner.company_id.minor_age_limit or 18
            partner.is_minor = bool(partner.age) and partner.age < limit
