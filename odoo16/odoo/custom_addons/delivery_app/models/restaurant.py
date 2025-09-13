from odoo import models, fields, api


class Restaurant(models.Model):
    _name = 'delivery.restaurant'
    _description = 'Restaurant'

    name = fields.Char(string='Restaurant Name' , required=True)
    restaurant_description = fields.Text(string='Restaurant Description')
    restaurant_city = fields.Char(compute='_compute_city', string='Restaurant City', required=True , store =1, readonly=0)
    restaurant_address = fields.One2many('address' , 'address_id' , string='Restaurant Address')
    restaurant_menu_item = fields.One2many('restaurant.menu' , 'menu_id' ,string='Restaurant Menu')


    _sql_constraints = [
        ('unique_name' , 'unique(name)' , 'This name is already exists'),
    ]

    @api.depends("restaurant_address.city")
    def _compute_city(self):
        for rec in self:
            rec.restaurant_city = ", ".join(rec.restaurant_address.mapped('city'))
            print(rec.restaurant_city)

