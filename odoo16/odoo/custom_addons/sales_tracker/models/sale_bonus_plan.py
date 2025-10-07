
from odoo import api, fields, models

class BonusPlan(models.Model):
    _name = 'sale.bonus.plan'
    _description = 'Sales Bonus Plan'
    _inherit = ['mail.thread' , 'mail.activity.mixin' ]


    name = fields.Char(required=True ,string='Name')
    start_date = fields.Date()
    end_date = fields.Date()
    bonus_type = fields.Selection([
        ('percentage','Percentage'),
        ('target','Target'),
    ], default='percentage')
    bonus_value = fields.Float()
    status = fields.Selection([
        ('draft','Draft'),
        ('active','Active'),
        ('closed','Closed')
    ], default='draft')

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is already in use')
    ]
    def action_closed_plan(self):
        self.ensure_one()
        domain = [('plan_id.id','=',self.ids)]
        print(self.ids)
        records = self.env['sale.bonus.record'].sudo().search(domain)
        records.unlink()
        for rec in self:
            rec.status = 'closed'

    def action_compute_bonus(self):
        print("inside action_compute_bonus")
        self.status = 'active'
        self.ensure_one()
        start , end= self.start_date , self.end_date
        domain = [('state','=','sale'),('date_order','>', start), ('date_order','<', end)]
        totals = {}
        print("_++++++++++++++++++++++++")
        orders = self.env['sale.order'].sudo().search(domain)
        print(orders)
        print("==========================")
        for o in orders:
            print('inside for orders')
            parent = o.user_id.partner_id
            print(parent)
            if not parent:
                continue
            totals.setdefault(parent.id , 0)
            totals[parent.id] += o.amount_total

        for pid , total in totals.items():
            bonus= 0
            if self.bonus_type == 'percentage':
                bonus = total * (self.bonus_value / 100)
            elif self.bonus_type == 'target':
                if total > 10000: bonus = self.bonus_value
                elif total > 5000: bonus = self.bonus_value/2
                else: bonus = 0

            self.env['sale.bonus.record'].sudo().create({
                'plan_id' : self.id,
                'partner_id' : pid ,
                'total_sales': total,
                'calculated_bonus' : bonus,
                'status' : 'draft',
            })