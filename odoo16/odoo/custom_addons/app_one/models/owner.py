

from odoo import models , fields

class Owner(models.Model):
    _name = 'owner'

    name = fields.Char(required = 1)
    phone = fields.Char(required = 1)
    address = fields.Char()
    property_ids = fields.One2many(comodel_name='property' , inverse_name='owner_id')


    def action_view_related_properties(self):
        self.ensure_one()
        return {
            'name' : "Related properties",
            'type' : "ir.actions.act_window",
            'res_model':"property",
            'view_mode':"tree,form",
            'domain' : [('id' , 'in' , self.property_ids.ids)],
            'target' : 'current',
        }