from odoo import models, fields,api
from datetime import timedelta

class OfficeProject(models.Model):
    _name = "office.project"
    _description = "Office Project"

    name = fields.Char(string="Project Name", required=True)
    employee_id = fields.Many2one("office.employee", string="Project Lead")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    deadline = fields.Date(string="Deadline")
    task = fields.Char(string='Task')
    employee_file = fields.Binary(string="Upload File")
    employee_file_name = fields.Char(string="File Name")


    task_ids = fields.One2many("office.task", "project_id", string="Tasks")

    def _default_start_date(self):
        return fields.Date.today()

    def _default_deadline(self):
        return fields.Date.today() + timedelta(days=30)

    @api.model
    def default_get(self, fields_list):
        res = super(OfficeProject, self).default_get(fields_list)
        res['start_date'] = fields.Date.today()
        res['deadline'] = fields.Date.today() + timedelta(days=15)  # auto set +15 days
        return res
