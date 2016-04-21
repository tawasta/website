# -*- coding: utf-8 -*-
from openerp import models, fields, api


class AttributionConfig(models.Model):
    _inherit = 'website.config.settings'

    attribution = fields.Char("Attribution message")

    # TODO: attribution setter
