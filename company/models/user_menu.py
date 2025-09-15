from odoo import models, fields, api

class UserMenus(models.Model):
    _name = 'user.menus'
    _description = 'User Menus'

    name = fields.Char(string="Concern Title", required=True)
    description = fields.Text(string="Concern Details")

    # Example function: print a message on create
    @api.model
    def create(self, vals):
        record = super(UserMenus, self).create(vals)
        # Custom logic here
        print(f"A new user menu was created: {record.name}")
        return record

    # Example button method
    def action_mark_done(self):
        # Example method to update a field or state
        for rec in self:
            rec.description = "Marked as done!"
