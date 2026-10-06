from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SlideChannel(models.Model):
    _inherit = "slide.channel"

    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        index=True,
        tracking=True,
        help="Leave empty to share the course with all companies.",
    )

    @api.onchange("website_id")
    def _onchange_website_id_set_company(self):
        if self.website_id:
            self.company_id = self.website_id.company_id

    @api.constrains("company_id", "website_id")
    def _check_website_company(self):
        for channel in self:
            website_company = channel.website_id.company_id
            if (
                channel.company_id
                and website_company
                and website_company != channel.company_id
            ):
                raise ValidationError(
                    _(
                        "The website of the course %(course)s belongs to "
                        "another company.",
                        course=channel.name,
                    )
                )


class SlideChannelPartner(models.Model):
    _inherit = "slide.channel.partner"

    company_id = fields.Many2one(
        "res.company",
        related="channel_id.company_id",
        store=True,
        index=True,
    )
