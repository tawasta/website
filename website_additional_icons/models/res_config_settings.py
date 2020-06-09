from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    # General
    favicon_svg = fields.Binary(
        string="Favicon SVG",
        related="website_id.favicon_svg",
        readonly=False
    )

    favicon_16 = fields.Binary(
        string="Favicon 16x16",
        related="website_id.favicon_16",
        readonly=False
    )

    favicon_32 = fields.Binary(
        string="Favicon 32x32",
        related="website_id.favicon_32",
        readonly=False
    )

    favicon_thumbnail_150 = fields.Binary(
        string="Favicon Thumbnail 150x150",
        related="website_id.favicon_thumbnail_150",
        readonly=False,
    )

    # Google
    favicon_48 = fields.Binary(
        string="Favicon 48x48",
        related="website_id.favicon_48",
        readonly=False
    )

    favicon_96 = fields.Binary(
        string="Favicon 96x96",
        related="website_id.favicon_96",
        readonly=False
    )

    favicon_144 = fields.Binary(
        string="Favicon 144x144",
        related="website_id.favicon_144",
        readonly=False
    )

    favicon_192 = fields.Binary(
        string="Favicon 192x192",
        related="website_id.favicon_192",
        readonly=False
    )

    favicon_256 = fields.Binary(
        string="Favicon 256x256",
        related="website_id.favicon_256",
        readonly=False
    )

    favicon_384 = fields.Binary(
        string="Favicon 384x384",
        related="website_id.favicon_384",
        readonly=False
    )

    favicon_512 = fields.Binary(
        string="Favicon 512x512",
        related="website_id.favicon_512",
        readonly=False
    )

    # Microsoft
    favicon_ico = fields.Binary(
        string="Favicon ICO",
        related="website_id.favicon_ico",
        readonly=False
    )

    favicon_ms_tile_126 = fields.Binary(
        string="Windows Tile 126x126",
        related="website_id.favicon_ms_tile_126",
        readonly=False
    )

    favicon_ms_tile_144 = fields.Binary(
        string="Windows Tile 144x144",
        related="website_id.favicon_ms_tile_144",
        readonly=False
    )

    favicon_ms_tile_270 = fields.Binary(
        string="Windows Tile 270x270",
        related="website_id.favicon_ms_tile_270",
        readonly=False
    )

    favicon_ms_tile_558_270 = fields.Binary(
        string="Windows Tile 558_270",
        related="website_id.favicon_ms_tile_558_270",
        readonly=False
    )

    favicon_ms_tile_558 = fields.Binary(
        string="Windows Tile 558x558",
        related="website_id.favicon_ms_tile_558",
        readonly=False
    )

    # Apple
    favicon_safari_pinned_svg = fields.Binary(
        string="Favicon Safari Pinned Tab SVG",
        related="website_id.favicon_safari_pinned_svg",
        readonly=False
    )

    favicon_57 = fields.Binary(
        string="Favicon 57x57",
        related="website_id.favicon_57",
        readonly=False
    )

    favicon_60 = fields.Binary(
        string="Favicon 60x60",
        related="website_id.favicon_60",
        readonly=False
    )

    favicon_72 = fields.Binary(
        string="Favicon 72x72",
        related="website_id.favicon_76",
        readonly=False
    )

    favicon_76 = fields.Binary(
        string="Favicon 76x76",
        related="website_id.favicon_76",
        readonly=False
    )

    favicon_114 = fields.Binary(
        string="Favicon 114x114",
        related="website_id.favicon_114",
        readonly=False
    )

    favicon_120 = fields.Binary(
        string="Favicon 120x120",
        related="website_id.favicon_120",
        readonly=False
    )

    favicon_152 = fields.Binary(
        string="Favicon 152x152",
        related="website_id.favicon_152",
        readonly=False
    )

    favicon_167 = fields.Binary(
        string="Favicon 167x167",
        related="website_id.favicon_167",
        readonly=False
    )

    favicon_180 = fields.Binary(
        string="Favicon 180x180",
        related="website_id.favicon_180",
        readonly=False
    )
