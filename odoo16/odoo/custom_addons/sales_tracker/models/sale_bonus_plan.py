from Tools.pynche.Main import docstring

from odoo import api, fields, models
from odoo.exceptions import ValidationError
class BonusPlan(models.Model):
    """
       Manages sales bonus plans.
       Handles configuration and computation of bonuses for salespersons
       based on sales orders, warehouse filters, and plan type.
    """
    _name = 'sale.bonus.plan'
    _description = 'Sales Bonus Plan'
    _inherit = ['mail.thread' , 'mail.activity.mixin' ]


    name = fields.Char(required=True ,string='Name')
    plan_type = fields.Selection([
        ('inclusive', 'Inclusive'),
        ('individual','Individual'),
    ] , default='inclusive')
    sale_person = fields.Many2one(
        'res.users' ,
        domain= lambda self : [('groups_id' , 'in' ,self.env.ref('sales_tracker.sales_tracker_sales_person').id)])
    start_date = fields.Date(default=fields.Date.today)
    end_date = fields.Date(default=fields.Date.today)
    bonus_type = fields.Selection([
        ('percentage','Percentage'),
        ('target','Target'),
    ], default='target')
    bonus_value = fields.Monetary(string='Bonus Value' ,currency_field="currency_id" )
    perc_value = fields.Char()
    status = fields.Selection([
        ('draft','Draft'),
        ('active','Active'),
        ('closed','Closed')
    ], default='draft')
    currency_id = fields.Many2one('res.currency', string='Currency' ,default=lambda self:self.env.company.currency_id.id)
    expense_account_id =fields.Many2one('account.account' , string='Expense Account' , required=True ,domain="[('account_type','=' ,'expense')]" )
    payable_account_id = fields.Many2one('account.account' , string='Payable Account' , required=True ,domain="[('account_type','=' ,'liability_payable')]" )
    journal_id = fields.Many2one('account.journal' , string='Journal' , required=True ,domain="[('type','=' ,'general')]" )
    moved_id = fields.Many2one('account.move' , string='Journal Entry')
    warehouse = fields.Selection([
        ('all' , 'All'),
        ('specific' , 'Specific ')
    ] , default='all')
    warehouse_id = fields.Many2one('stock.warehouse' , string='WareHouse')

    @api.onchange('bonus_type' , 'perc_value')
    def remove_currency(self):
        """
        Returns: % symbol or currency symbol next to field (bonus_value)
        """
        for rec in self:
            if rec.bonus_type == 'percentage':
                pct_currency = self.env['res.currency'].search([('symbol', '=', '%')], limit=1)
                if pct_currency:
                    rec.currency_id = pct_currency.id
            else:
                rec.currency_id = self.env.company.currency_id.id

    @api.constrains('name')
    def _check_name(self):
        """
        Returns: Restrict the name to prevent duplication
        """
        for rec in self:
            existing = self.search([
                ('name', '=', rec.name),
                ('id', '!=', rec.id)
            ])
            if existing:
                raise ValidationError(f"The name '{rec.name}' already exists.")

    @api.onchange('start_date' , 'end_date')
    def check_date_value(self):
        """
        Returns: User error interface to Consideration the time rules
        """
        today_date = fields.Date.context_today(self)
        for rec in self:
            print(today_date)
            print("+++++++++++++")
            if rec.start_date > today_date:
                raise ValidationError('Start date must be before or equal today date')
            if rec.end_date < rec.start_date:
                raise ValidationError('End date must be after or equal start date')

    def action_closed_plan(self):
        """
        Returns: Closed plan Change status of plan to closed and Delete all record are connected with it
        """
        self.ensure_one()
        domain = [('plan_id.id','=',self.ids)]
        print(self.ids)
        records = self.env['sale.bonus.record'].sudo().search(domain)
        records.unlink()
        for rec in self:
            rec.status = 'closed'


    def action_compute_bonus(self):
        """

        Returns:Compute and generate bonus records for each salesperson.

        """
        print("inside action_compute_bonus")
        self.status = 'active'
        self.ensure_one()
        start , end , wareHouse , salesperson= self.start_date , self.end_date , self.warehouse_id , self.sale_person
        primary_domain = [('state','=','sale'),('date_order','>', start), ('date_order','<', end)]
        secondary_domain = [
            ('state','=','sale'),
            ('date_order','>', start),
            ('date_order','<', end) ,
            ('warehouse_id','=',wareHouse.id)]

        domain = []
        if self.warehouse == 'all' :
            if self.plan_type=='inclusive':
                domain = primary_domain
            else:
                if not self.sale_person:
                    raise ValidationError("You must specify a sale_person")
                else:
                    domain = primary_domain + [('user_id.partner_id' ,'=' , salesperson.partner_id.id)]
        else:
            if not self.warehouse_id:
                raise ValidationError("You must specify a warehouse_id")
            else:
                if self.plan_type=='inclusive':
                    domain = secondary_domain
                else:
                    domain= secondary_domain + [('user_id.partner_id' , '=' , salesperson.partner_id.id)]

        totals = {}
        print("_++++++++++++++++++++++++")
        print("+++" + f"{domain}" + "++++++")
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
        print("==========================")
        print(totals)
        print("==========================")

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