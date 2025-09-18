from odoo import models, fields,api
from odoo.exceptions import UserError,ValidationError

class OfficeEmployee(models.Model):
    _name = "office.employee"
    _description = "Office Employee"

    name = fields.Char(string="Employee Name", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    department_id = fields.Many2one("office.department", string="Department")
    location = fields.Char(string="Location")
    join_data = fields.Date(string="Join Date")
    employee_file = fields.Binary(string="Upload File")
    employee_file_name = fields.Char(string="File Name")

    project_ids = fields.One2many("office.project", "employee_id", string="Projects")

    @api.constrains('email')
    def _check_email_format(self):
        email_pattern = r"[^@]+@[^@]+\.[^@]+"
        for record in self:
            if record.email and not re.match(email_pattern, record.email):
                raise ValidationError("Invalid email format: %s" % record.email)