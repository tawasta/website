from odoo import api
from odoo import fields
from odoo import models


class Slide(models.Model):

    _inherit = "slide.slide"

    datas_filename = fields.Char("Slide filename")

    @api.multi
    def write(self, values):
        print(values)
        if values.get("datas") and not values.get("index_content"):
            # If the file is changed, remove incorrect indexed content
            # TODO: recreate indexed content
            values["index_content"] = False

        return super(Slide, self).write(values)
