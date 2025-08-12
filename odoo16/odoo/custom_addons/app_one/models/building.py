from pkg_resources import require

from odoo import models , fields ,api

class Building(models.Model):
    _name = 'building'
    _description = "building Record"
    _inherit = ['mail.thread' , 'mail.activity.mixin' ]


    no = fields.Integer()
    code =fields.Char()
    description  = fields.Text()
    name = fields.Char()
    active = fields.Boolean()

