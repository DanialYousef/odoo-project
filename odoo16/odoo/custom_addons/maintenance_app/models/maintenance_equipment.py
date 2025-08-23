from tokenize import String

from odoo import api, fields, models
from datetime import date, timedelta
from odoo.exceptions import ValidationError


class MaintenanceEquipment(models.Model):
    _name = 'maintenance.equipment'
    _description = 'Maintenance Equipment'

    name = fields.Char(String='Equipment Name', required=True)
    serial_number = fields.Char(string='Serial Number', required=True)
    owner_id = fields.Many2one('res.partner', string='Owner', required=True)
    last_maintenance_date = fields.Date(string='Last Maintenance Date')
    next_maintenance_date = fields.Date(string='Next Maintenance Date')
    maintenance_request_ids = fields.One2many(
        'maintenance.request',
        'equipment_id',
        string='Maintenance Requests'
    )

    _sql_constraints = [
        ('unique_serial_number', 'unique(serial_number)', 'This serial number is already in use!')
    ]

    @api.constrains('last_maintenance_date')
    def _check_last_maintenance_date(self):
        for rec in self:
            if rec.last_maintenance_date > date.today():
                raise ValidationError('Last Maintenance Date cannot be in the future')

    @api.constrains('next_maintenance_date')
    def _check_next_maintenance_date(self):
        for rec in self:
            if rec.next_maintenance_date < date.today():
                raise ValidationError('Next Maintenance Date cannot be in the past')




    @api.model
    def run_scheduled_maintenance_check(self):
        today = date.today()

        equipment_ids  = self.search([
            ('next_maintenance_date', '<=', today),
            ('next_maintenance_date', '!=', False)
        ])

        for equipment_id in equipment_ids:
            self.env['maintenance.request'].create({
                'name': f'Scheduled Maintenance for {equipment_id.name}',
                'description': f'This is a routine maintenance check for the equipment {equipment_id.name}.',
                'equipment_id': equipment_id.id,
                'request_date': fields.Date.today(),
            })
            equipment_id.next_maintenance_date = today + timedelta(days=365)