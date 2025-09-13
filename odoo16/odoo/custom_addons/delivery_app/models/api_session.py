from odoo import models, fields

class ApiSession(models.TransientModel):
    _name = 'api.session'
    _description = 'API Session'

    token = fields.Char(string='Token', required=True, copy=False)
    customer_id = fields.Many2one('delivery.customer', string='Customer', required=True, ondelete='cascade')
    expiration_time = fields.Datetime(string='Expiration Time')