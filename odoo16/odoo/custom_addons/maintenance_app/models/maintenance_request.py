from odoo import api, fields, models

class MaintenanceRequest(models.Model):
    _name = 'maintenance.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Maintenance Request'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    request_date = fields.Datetime(string='Request Date', default=fields.Datetime.now, required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Canceled'),
    ], default='draft', string='Status', required=True)

    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment', required=True)


    def action_in_progress(self):
        for rec in self:
            rec.state = 'in_progress'
    def action_done(self):
        for rec in self:
            rec.state = 'done'
    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
    def action_in_progress(self):
        for rec in self:
            rec.state = 'in_progress'

    def action_to_finish_process(self):
        action = self.env['ir.actions.actions']._for_xml_id('maintenance_app.action_change_state_in_main')
        action['context'] = {'default_maintenance_ids' : self.ids}
        return action
