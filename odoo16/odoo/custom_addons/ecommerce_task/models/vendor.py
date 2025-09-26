from odoo import api, fields, models

class Vendor(models.Model):
    _inherit = 'res.partner'

    is_vendor = fields.Boolean(String="Is a Vendor", default=False)

