from odoo import models, fields

class EcommerceDiscount(models.Model):
    _name = 'ecommerce.discount'
    _description = 'Ecommerce Discount Rules'

    name = fields.Char(string='Discount Name', required=True)
    discount_type = fields.Selection([
        ('percentage', 'Percentage'),
        ('fixed_amount', 'Fixed Amount')
    ], string='Discount Type', required=True, default='percentage')
    discount_value = fields.Float(string='Discount Value', required=True)
    apply_on_all_vendors = fields.Boolean(string='Apply on All Vendors', default=False)
    vendor_id = fields.Many2one('res.partner', string='Specific Vendor', domain=[('is_vendor', '=', True)],
                                help="Leave empty to apply on all vendors if 'Apply on All Vendors' is checked.")

    _sql_constraints = [
        ('check_discount_value', 'CHECK(discount_value >= 0)', 'The discount value must be a positive number.'),
    ]