from odoo import models, fields, api

class Address(models.Model):
    _name = 'address'
    _description = 'Address'

    name = fields.Char(string='Address Name' , required=True)
    city = fields.Char(string='City' , required=True)
    phonenumbers = fields.Char(string='Phone Number' , required=True)
    street = fields.Char(string='Street' , required=True)
    address_id = fields.Many2one('delivery.restaurant')
    customer_id = fields.Many2one('delivery.customer')

