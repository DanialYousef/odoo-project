from odoo import models, fields, api

class RestaurantMenu(models.Model):
    _name = 'restaurant.menu'
    _description = 'Restaurant Menu'

    name = fields.Char(string='Menu Name' , required=True)
    description = fields.Text(string='Menu Description')
    type_of_food = fields.Selection([
        ('fast_food' , 'Fast Food' ),
        ('vegetarian food' , 'Vegetarian Food' ),
        ('seafood' , 'Seafood' ),
        ('other' , 'Other' ),
    ] , default='other' , string='Menu Type')
    making_time = fields.Float(string='Making Time' , required=True)
    menu_id = fields.Many2one('delivery.restaurant' , string='Restaurant Name' )
    delivery_order_id = fields.Many2one('delivery.order' , string='Restaurant Menu Order' )