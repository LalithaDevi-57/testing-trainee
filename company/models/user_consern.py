# my_module/models/user_concern.py

from odoo import models, fields,api

class UserConcern(models.Model):
    _name = 'user.concern'
    _description = 'User Concern'

    name = fields.Char(string='Concern Title', required=True)
    description = fields.Text(string='Description')
    user_id = fields.Many2one('res.users', string='User')
    state = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved')
    ], default='open')

    @api.model
    def create(self, vals):
        if 'user_id' not in vals:
            vals['user_id'] = self.env.uid
        return super(UserConcern, self).create(vals)

