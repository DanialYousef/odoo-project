

from odoo import models , fields , api
from odoo.exceptions import ValidationError

class TodoModel(models.Model):
    _name='todo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Todo Record'

    name=fields.Char()
    description = fields.Text()
    date = fields.Date()
    res_partner = fields.Many2one('res.partner' , default=lambda self: self.env.user.partner_id)
    lines_ids = fields.One2many('todo.lines'  , 'todo_id')
    total_hour = fields.Float(default=5)
    state = fields.Selection([
        ('new' , 'New'),
        ('in_progress' , 'In Progress'),
        ('completed', 'Completed'),
        ('closed' , 'Closed')
      ] , default='new'
    )

    def action_new(self):
        for rec in self:
            rec.state = 'new'

    def action_in_progress(self):
        for rec in self:
            rec.state = 'in_progress'

    def action_completed(self):
        for rec in self:
            rec.state = 'completed'

    def action_closed(self):
        for rec in self:
            rec.state = 'closed'

    @api.constrains('lines_ids')
    def _check_sum_of_hour(self):
        sum = 0
        for rec in self:
            for line in rec.lines_ids:
                sum += line.hours
                if sum > rec.total_hour:
                    raise ValidationError("Total hour cannot be more than total hour")

    def change_action_users_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('todo_app.action_change_partner_wizard')
        action['context'] = {'default_todo_ids': self.ids}
        return action
class TodoLines(models.Model):
    _name='todo.lines'

    description = fields.Text()
    hours = fields.Integer(default=0)
    todo_id = fields.Many2one('todo')