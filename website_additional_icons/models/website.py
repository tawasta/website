from odoo import models, fields


class Website(models.Model):

    _inherit = "website"

    # General
    favicon_svg = fields.Binary(
        string="SVG Favicon",
    )

    favicon_16 = fields.Binary(
        string="16x16 Favicon",
    )

    favicon_32 = fields.Binary(
        string="32x32 Favicon",
    )

    favicon_thumbnail_150 = fields.Binary(
        string="150x150 Thumbnail"
    )

    # Google
    favicon_48 = fields.Binary(
        string="48x48 Favicon",
    )

    favicon_96 = fields.Binary(
        string="96x96 Favicon",
    )

    favicon_144 = fields.Binary(
        string="144x144 Favicon",
    )

    favicon_192 = fields.Binary(
        string="192x192 Favicon",
    )

    favicon_256 = fields.Binary(
        string="256x256 Favicon",
    )

    favicon_384 = fields.Binary(
        string="384x384 Favicon",
    )

    favicon_512 = fields.Binary(
        string="512x512 Favicon",
    )

    # Microsoft
    favicon_ico = fields.Binary(
        string="ICO Favicon",
    )

    favicon_ms_tile_126 = fields.Binary(
        string="Windows Tile 126x126",
    )

    favicon_ms_tile_144 = fields.Binary(
        string="Windows Tile 144x144",
    )

    favicon_ms_tile_270 = fields.Binary(
        string="Windows Tile 270x270",
    )

    favicon_ms_tile_558_270 = fields.Binary(
        string="Windows Tile 558x270",
    )

    favicon_ms_tile_558 = fields.Binary(
        string="Windows Tile 558x558",
    )

    # Apple
    favicon_safari_pinned_svg = fields.Binary(
        string="Safari pinned tab svg favicon",
    )

    favicon_57 = fields.Binary(
        string="57x57 Favicon",
    )

    favicon_60 = fields.Binary(
        string="60x60 Favicon",
    )

    favicon_72 = fields.Binary(
        string="72x72 Favicon",
    )

    favicon_76 = fields.Binary(
        string="76x76 Favicon",
    )

    favicon_114 = fields.Binary(
        string="114x114 Favicon",
    )

    favicon_120 = fields.Binary(
        string="120x120 Favicon",
    )

    favicon_152 = fields.Binary(
        string="152x152 Favicon",
    )

    favicon_167 = fields.Binary(
        string="167x167 Favicon",
    )

    favicon_180 = fields.Binary(
        string="180x180 Favicon",
    )
