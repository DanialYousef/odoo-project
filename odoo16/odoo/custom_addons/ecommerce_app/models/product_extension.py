from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_category_type = fields.Selection([
        ('books', 'Books'),
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('other', 'Other'),
    ], string='Product Category', default='other')