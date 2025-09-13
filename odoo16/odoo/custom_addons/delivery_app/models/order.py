from odoo import models, fields


class DeliveryOrder(models.Model):
    _name = 'delivery.order'
    _description = 'Delivery Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Order ID', required=True)
    order_date = fields.Datetime(string='Order Date', default=fields.Datetime.now)
    customer_id = fields.Many2one('delivery.customer', string='Customer', required=True)
    delivery_person_id = fields.Many2one('res.users', string='Delivery Person')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ], default='pending', string='Status', required=True)
    order_lines = fields.One2many('restaurant.menu' , inverse_name='delivery_order_id', string='Order Lines' )

    def action_pending(self):
        for rec in self:
            rec.state = 'pending'

    def action_accepted(self):
        for rec in self:
            rec.state = 'accepted'

    def action_out_for_delivery(self):
        for rec in self:
            rec.state = 'out_for_delivery'

    def action_delivered(self):
        for rec in self:
            rec.state = 'delivered'

    def action_canceled(self):
        for rec in self:
            rec.state = 'canceled'

class DeliveryOrderLine(models.Model):
    _name = 'delivery.order.line'
    _description = 'Order Line'

    quantity = fields.Integer(string='Quantity', required=True)
    order_id = fields.Many2one('delivery.order', string='Order', required=True)
    description = fields.Char(String="Description")


class DeliveryPerson(models.Model):
    _inherit = 'res.users'

    is_delivery_person = fields.Boolean(string='Is a Delivery Person', default=False)
    is_available = fields.Boolean(string='Is Available', default=True)