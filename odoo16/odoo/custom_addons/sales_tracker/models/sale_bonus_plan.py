
from odoo import api, fields, models
from odoo.exceptions import ValidationError

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
    bonus_value = fields.Monetary(string='Bonus Value' ,currency_field="currency_id" )
    status = fields.Selection([
        ('draft','Draft'),
        ('active','Active'),
        ('closed','Closed')
    ], default='draft')
    currency_id = fields.Many2one('res.currency', string='Currency' ,default=lambda self:self.env.company.currency_id.id)
    expense_account_id =fields.Many2one('account.account' , string='Expense Account' , required=True )
    payable_account_id = fields.Many2one('account.account' , string='Payable Account' , required=True )
    journal_id = fields.Many2one('account.journal' , string='Journal' , required=True )
    moved_id = fields.Many2one('account.move' , string='Journal Entry'  )

    """ Create a restriction that prevents duplication of an existing name """
    @api.constrains('name')
    def _check_name(self):
        for rec in self:
            existing = self.search([
                ('name', '=', rec.name),
                ('id', '!=', rec.id)
            ])
            if existing:
                raise ValidationError(f"The name '{rec.name}' already exists.")


    """ Closed plan : Change status of plan to closed and Delete all record are connected with it  """
    def action_closed_plan(self):
        self.ensure_one()
        domain = [('plan_id.id','=',self.ids)]
        print(self.ids)
        records = self.env['sale.bonus.record'].sudo().search(domain)
        records.unlink()
        for rec in self:
            rec.status = 'closed'


    """ Compute Bonus : Get All Sale Orders and Calculate Bonsu Depending on Total sales of each representative individually """
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

        high_total = 10000
        min_total = 5000
        for pid, total in totals.items():
            bonus = 0
            if self.bonus_type == 'percentage':
                bonus = total * (self.bonus_value / 100)
            elif self.bonus_type == 'target':
                if total > high_total:
                    bonus = self.bonus_value
                elif total > min_total:
                    bonus = self.bonus_value / 2
                else:
                    bonus = 0

            self.env['sale.bonus.record'].sudo().create({
                'plan_id' : self.id,
                'partner_id' : pid ,
                'total_sales': total,
                'calculated_bonus' : bonus,
                'status' : 'draft',
                'expense_account_id' : self.expense_account_id.id,
                'payable_account_id' : self.payable_account_id.id,
                'journal_id' : self.journal_id.id,
            })