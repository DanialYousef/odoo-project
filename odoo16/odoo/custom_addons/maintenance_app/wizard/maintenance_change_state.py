from odoo import api, fields, models
from odoo.exceptions import ValidationError
class MaintenanceApp(models.TransientModel):
    _name = 'maintenance.change.state'
    _description = 'Maintenance Change State'

    maintenance_ids = fields.Many2many('maintenance.request' , string='Maintenance Requests')
    new_state = fields.Selection([
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ])


    def confirm_action_change_state(self):
        print('inside condition if')
        for request in self.maintenance_ids:
            if request.state == 'in_progress':
                print('inside condition if')
                request.state = self.new_state
            else:
                raise ValidationError('Maintenance Request state is not in_progress')