import requests
from pkg_resources import require

from odoo import models , fields ,api
from odoo.exceptions import ValidationError

class Property(models.Model):
    _name = 'property'
    _description = "Property Record"
    _inherit = ['mail.thread' , 'mail.activity.mixin' ]

    name = fields.Char(required=1 )
    ref = fields.Char(default='ref', readonly=1)
    active = fields.Boolean(default=True)
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=1)
    data_availability = fields.Date(tracking=1)
    data_selling_expected = fields.Date()
    is_late = fields.Boolean()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff' , store =1 , readonly=0)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    owner_address = fields.Char(related='owner_id.address' , readonly=0)
    owner_phone = fields.Char(related='owner_id.phone', readonly=0)
    garden_orientation = fields.Selection([
        ('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West'),
    ])

    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    state = fields.Selection(
        [
            ('draft','Draft'),
            ('pending' ,'Pending'),
            ('sold' ,'Sold'),
            ('closed' , 'Closed')

        ],
        default='draft',
    )
    line_ids = fields.One2many('property.line' , 'property_id')

    _sql_constraints = [
        ('unique_name','unique("name")','This name is already in use')
    ]
    @api.depends('expected_price' , 'selling_price' )
    def _compute_diff(self):
        for rec in self:
            print('inside _compute_diff')
            rec.diff = rec.expected_price - rec.selling_price

    @api.onchange('expected_price' , 'selling_price' , 'owner_id.phone')
    def _onchange_phone(self):
        for rec in self:
            print('inside  _onchange_phone')
            return {
                'warning' : {'title' : 'warning' , 'message' : 'negative value.' , 'type' : 'notification' },
            }

    def action_search(self):
        print(self.env['property'].search([('name' , '=' , 'property 1')]))

    @api.constrains('bedrooms')
    def _check_bedrooms(self):
        for rec in self:
            if rec.bedrooms == 0 :
                raise ValidationError("Bedrooms cannot be 0")

    def create_property_history(self , old_state , new_state , reason):
        for rec in self:
            rec.env['property.history'].create({
                'user_id' : rec.env.uid ,
                'property_id' : rec.id ,
                'old_state' : old_state,
                'new_state' : new_state,
                'reason' : reason or '',
                'line_ids' : [(0,0,{'description' : line.description , 'area' : line.area})for line in rec.line_ids]
            })

    def actions_draft(self):
        for rec in self:
            print(rec)
            rec.create_property_history(rec.state , 'draft' , '')
            rec.state = 'draft'

    def actions_pending(self):
        for rec in self:
            rec.create_property_history(rec.state , 'pending' ,'')

            rec.state = 'pending'

    def actions_sold(self):
        for rec in self:
            rec.create_property_history(rec.state , 'sold' , '')

            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.create_property_history(rec.state , 'closed' , '')
            rec.state = 'closed'

    def action_selling_expected(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.data_selling_expected and rec.data_selling_expected < fields.date.today():
                rec.is_late = True


    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)
        res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res

    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.change_state_action')
        action['context'] = {'default_property_id' : self.id}
        return action

    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id = self.env.ref('app_one.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id , 'form']]
        return action

    # @api.model
    # def search(self, domain, offset=0, limit=None, order=None, count=False):
    #     res = super(Property, self).search(domain, offset, limit, order, count)
    #     print("inside search method")
    #     return res
    #
    # def write(self, vals):
    #     res = super(Property , self).write(vals)
    #     print("inside write method")
    #     return res
    #
    # def unlink(self):
    #     res =super(Property , self).unlink()
    #     print("inside unlink method")
    #     return res

    def action_test_api(self):
        payload =dict()
        try:
            response = requests.get("http://localhost:8069/v1/property/list", data=payload)
            print(response.content)
            if response.status_code == 200:
                print("successfully")
            else:
                print("failer")
        except Exception as error:
            raise ValidationError(str(error))

    def generate_excel_reports(self):
        return {
            "type" : "ir.actions.act_url",
            "url" : f'/property/excel/report/{self.env.context.get("active_ids")}',
            "target" : 'new'
        }

class PropertyLine(models.Model):
    _name = 'property.line'

    area = fields.Float()
    description = fields.Char()
    property_id = fields.Many2one('property')
