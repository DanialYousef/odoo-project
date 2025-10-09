from odoo import fields, models , api
from odoo.exceptions import ValidationError


class BonusRecord(models.Model):
    _name = 'sale.bonus.record'
    _inherit = ['mail.thread' , 'mail.activity.mixin' ]

    plan_id = fields.Many2one('sale.bonus.plan', required=True)
    partner_id = fields.Many2one('res.partner')
    total_sales = fields.Monetary(string='Total Sales' , currency_field="currency_id")
    calculated_bonus = fields.Monetary(string='Calculated Bonus' , currency_field="currency_id")
    currency_id = fields.Many2one('res.currency', string='Currency' , default=lambda self : self.env.company.currency_id.id)
    status = fields.Selection([
        ('draft','Draft'),
        ('approved','Approved')
    ], default='draft')
    expense_account_id =fields.Many2one('account.account' , string='Expense Account' , required=True )
    payable_account_id = fields.Many2one('account.account' , string='Payable Account' , required=True )
    journal_id = fields.Many2one('account.journal' , string='Journal' , required=True )
    moved_id = fields.Many2one('account.move' , string='Journal Entry' )
    is_canceled = fields.Boolean(string='Is Canceled' , default=False)

    """ Approved plan : Check tha result by manger ,
     Update result and approved the plan to create financial restriction in Accounting module """
    def action_approved_state(self):
        print(self.plan_id.id)
        for rec in self:
            try:
                move_vals = {
                    'invoice_date' : fields.Date.context_today(self),
                    'ref' : f'bonus - {rec.partner_id.name}',
                    'journal_id' : rec.journal_id.id,
                    'line_ids' : [
                        (0,0,{
                            'name' : f'bonus expense for {rec.partner_id.name}',
                            'account_id' : rec.expense_account_id.id,
                            'debit' : rec.calculated_bonus,
                            'credit' : 0,
                        }),
                        (0,0,{
                            'name': f'Bonus Payable to {rec.partner_id.name}',
                            'account_id': rec.payable_account_id.id,
                            'debit': 0.0,
                            'credit': rec.calculated_bonus,
                            'partner_id': rec.partner_id.id,
                        })
                    ]
                }
                move = self.env['account.move'].create(move_vals)
                move.action_post()

                rec.write({
                    'status': 'approved',
                    'moved_id': move.id,
                })
            except Exception as error:
                raise ValidationError(str(error))

    """ Change the value of column (is_canceled) of the open record """
    def action_archive_state(self):
        print('inside action archive state')
        for rec in self:
            rec.is_canceled = True

