from odoo import models , fields , api

class PropertyHistory(models.Model):
    _name = 'property.history'

    user_id = fields.Many2one('res.partner')
    property_id = fields.Many2one('property')
    old_state = fields.Char()
    new_state= fields.Char()
    reason = fields.Char()
    line_ids = fields.One2many(comodel_name= 'property.history.line',inverse_name='property_id',string='Line')


class PropertyHistoryLine(models.TransientModel):
    _name = 'property.history.line'

    area = fields.Float()
    description = fields.Char()
    property_id = fields.Many2one('property.history')
