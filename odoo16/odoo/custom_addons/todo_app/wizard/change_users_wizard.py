from odoo import models ,fields
from odoo.exceptions import ValidationError

class ChangeUsersWizard(models.TransientModel):
    _name = "change.users.wizard"

    todo_ids = fields.Many2many('todo', string='Assign To')
    new_res_partner = fields.Many2one('res.partner' , required=True)



    def action_confirm_wizard(self):
        for todo in self.todo_ids:
            print("inside action")
            if todo.state in ('new', 'in_progress'):
                todo.res_partner = self.new_res_partner
            else:
                raise  ValidationError("value of state must be 'new' or 'in_progress'")



