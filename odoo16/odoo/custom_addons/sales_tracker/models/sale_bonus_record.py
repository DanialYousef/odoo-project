from odoo import fields, models

class BonusRecord(models.Model):
    _name = 'sale.bonus.record'
    _inherit = ['mail.thread' , 'mail.activity.mixin' ]

    plan_id = fields.Many2one('sale.bonus.plan', required=True)
    partner_id = fields.Many2one('res.partner', required=True)
    total_sales = fields.Float(string='Total Sales')
    calculated_bonus = fields.Float(string='Calculated Bonus')
    status = fields.Selection([
        ('draft','Draft'),
        ('approved','Approved')
    ], default='draft')

    def action_approved_state(self):
        print(self.plan_id.id)
        for rec in self:
            rec.status = 'approved'
