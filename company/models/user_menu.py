from odoo import models, fields, api

class UserMenus(models.Model):
    _name = 'user.menus'
    _description = 'User Menus'

    name = fields.Char(string="Concern Title", required=True)
    description = fields.Text(string="Concern Details")
    # @api.model
    # def create(self, vals):
    #     record = super(UserMenus, self).create(vals)
    #     print(f"A new user menu was created: {record.name}")
    #     return record
    #
    # def action_mark_done(self):
    #     for rec in self:
    #         rec.description = "Marked as done!"
