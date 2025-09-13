from odoo import models, fields, api
import uuid

class Customer(models.Model):
    _name = 'delivery.customer'
    _description = 'Delivery Customer'

    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string='Phone Number')
    email = fields.Char(string='Email', required=True, unique=True)
    password = fields.Char(string='Password')
    address_ids = fields.One2many('address', 'customer_id', string='Addresses')
