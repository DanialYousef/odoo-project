from odoo import models , fields , api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_do_somthing(self):
        print(self , "action_do_somthing")