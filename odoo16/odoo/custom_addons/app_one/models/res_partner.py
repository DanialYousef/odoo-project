from odoo import models , fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(string='Name', readonly=True)
    property_id = fields.Many2one('property')

