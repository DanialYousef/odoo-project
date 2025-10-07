from odoo import models, fields, api

class ProductVariantQtyLine(models.TransientModel):
    _name = 'product.variant.qty.line'
    _description = "Variant Quantity Line"

    template_id = fields.Many2one('product.template', string="Template")
    variant_id = fields.Many2one('product.product', string="Variant")
    variant_name = fields.Char(string="Variant Name")
    qty_available = fields.Float(string="Available Qty")

class Product(models.Model):
    _inherit = "product.template"

    vendor_id = fields.Many2one('res.partner', string="Vendor" ,domain=[('is_vendor','=',True)])
    is_variant_product  = fields.Boolean(string="Has Variant", compute="_compute_is_variant_product" , store=True)

    variant_qty_text = fields.Text(
        string="Variants Quantities",
        compute="_compute_variant_qty_text"
    )

    @api.depends('product_variant_ids.qty_available')
    def _compute_variant_qty_text(self):
        for template in self:
            lines = []
            for v in template.product_variant_ids:
                name = v.display_name
                qty = v.qty_available
                lines.append(f"{name}: {qty}")
            template.variant_qty_text = "\n".join(lines) if lines else ""


    variant_qty_lines = fields.One2many(
        'product.variant.qty.line',
        'template_id',
        string="Variant Quantities",
        compute="_compute_variant_qty_lines",
        store=False
    )

    @api.depends('product_variant_ids.qty_available')
    def _compute_variant_qty_lines(self):
        VariantQtyLine = self.env['product.variant.qty.line']
        for template in self:
            template.variant_qty_lines = False
            lines = []
            for variant in template.product_variant_ids:
                line_vals = {
                    'template_id': template.id,
                    'variant_id': variant.id,
                    'variant_name': variant.display_name,
                    'qty_available': variant.qty_available,
                }
                lines.append((0, 0, line_vals))
            template.variant_qty_lines = lines

    discounted_price = fields.Float(
        string='Discounted Price',
        compute='_compute_discounted_price',
        store=True
    )
    attribute_value_ids = fields.Many2many(
        'product.attribute.value',
        string="Attribute Values",
        compute='_compute_attribute_value_ids'
    )

    selected_attribute_value_id = fields.Many2one(
        'product.attribute.value',
        string="Select Variant Attribute",
    )
    quantity_of_selected_variant = fields.Integer(
        string="Quantity On Hand",
        compute='_compute_quantity_of_selected_variant')

    @api.depends('attribute_line_ids.value_ids')
    def _compute_attribute_value_ids(self):
        for rec in self:
            rec.attribute_value_ids = rec.attribute_line_ids.mapped('value_ids')

    @api.depends('selected_attribute_value_id', 'product_variant_ids.qty_available')
    def _compute_quantity_of_selected_variant(self):
        for product in self:
            product.quantity_of_selected_variant = 0
            if product.selected_attribute_value_id:
                variant = product.product_variant_ids.filtered(
                    lambda p: product.selected_attribute_value_id in p.product_template_attribute_value_ids.mapped(
                        'product_attribute_value_id')
                )
                if variant:
                    product.quantity_of_selected_variant = sum(variant.mapped('qty_available'))

    @api.depends('list_price', 'vendor_id')
    def _compute_discounted_price(self):
        for product in self:
            discount = self.env['ecommerce.discount'].sudo().search([
                '|',
                ('apply_on_all_vendors', '=', True),
                ('vendor_id', '=', product.vendor_id.id)
            ], limit=1)

            if discount and discount.discount_type == 'percentage':
                product.discounted_price = product.list_price * (1 - discount.discount_value / 100)
            elif discount and discount.discount_type == 'fixed_amount':
                product.discounted_price = product.list_price - discount.discount_value
            else:
                product.discounted_price = product.list_price

    def _compute_is_variant_product(self):
        for product in self:
            product.is_variant_product = len(product.attribute_line_ids) > 0

class ProductProduct(models.Model):
    _inherit = 'product.product'
