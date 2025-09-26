# ecommerce_task/models/pricelist_extension.py
from odoo import models, fields

class PricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    applied_on = fields.Selection(
        selection_add=[('1_vendor', 'Vendor')],
        ondelete={'1_vendor': 'set default'}
    )
    vendor_id = fields.Many2one(
        'res.partner',
        string="Vendor",
        domain=[('is_vendor', '=', True)],
        help="Pricelist applies to products from this specific vendor."
    )

    #override to add vendor domain
    def _get_item_domain(self):
        domain = super(PricelistItem, self)._get_item_domain()
        if self.applied_on == '1_vendor' and self.vendor_id:
            domain.append(('vendor_id', '=', self.vendor_id.id))
        return domain