from odoo import models
from odoo.osv import expression

class Website(models.Model):
    _inherit = 'website'

    def website_domain(self, website_id=False, m2m_field=None):
        """Backwards compatible extension of the core helper.

        When *m2m_field* (e.g. 'visible_website_ids') is provided, return a domain
        matching records where that M2M is either empty (visible on all websites)
        or contains the given/current website. Otherwise, defer to core behavior.
        """
        if not m2m_field:
            return super().website_domain(website_id)

        wid = website_id or self.id
        return expression.OR([
            [(m2m_field, '=', False)],
            [(m2m_field, 'in', wid)],
        ])
