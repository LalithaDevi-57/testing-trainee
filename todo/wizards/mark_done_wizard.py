
from odoo import models, fields
from datetime import date ,timedelta

class MarkDoneWizard(models.TransientModel):
    _name = 'todo.mark.done.wizard'
    _description = 'Mark Selected Tasks as Done'

    from_date = fields.Date(string='From', required=True)
    task_ids = fields.Many2many('todo.task', string='Tasks')
    name =fields.Text(string='Task Name')
    today = fields.Date(string='To', default=lambda self: date.today(), readonly=True)

    def action_mark_as_done(self):
        for task in self.task_ids:
            task.is_done = True