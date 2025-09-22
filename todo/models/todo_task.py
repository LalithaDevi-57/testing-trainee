from odoo import models, fields

class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'ToDo Task'

    name = fields.Char(required=True)
    description = fields.Text()
    due_date = fields.Date()
    is_done = fields.Boolean(default=False)