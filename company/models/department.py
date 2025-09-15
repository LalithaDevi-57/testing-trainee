from odoo import models, fields,api
from datetime import datetime,timedelta

class OfficeDepartment(models.Model):
    _name = "office.department"
    _description = "Office Department"

    name = fields.Char(string="Department Name", required=True)
    manager_id = fields.Many2one("office.employee", string="Manager")
    location = fields.Char(string="Location")
    join_data = fields.Date(string="Join Date")

    employee_ids = fields.One2many("office.employee", "department_id", string="Employees")

    type = fields.Char(string='Department Type')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'type' in fields_list:
            res['type'] = 'Finance'
        return res