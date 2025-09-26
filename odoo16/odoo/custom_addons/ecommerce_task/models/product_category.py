from odoo import fields, models

class ProductCategory(models.Model):
    _inherit = "product.category"

    vendor_id = fields.Many2one("res.partner" , string="Vendor Id" , domain=[('is_vendor','=',True)])