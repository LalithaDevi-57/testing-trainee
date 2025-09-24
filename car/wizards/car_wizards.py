from odoo import models, fields, api

class CarWizard(models.TransientModel):
    _name = 'car.wizard'
    _description = 'Car Model Wizard'

    name = fields.Char(string='Car Name')
    price = fields.Float(string='Unit Price')
    quantity = fields.Float(string='Quantity')
    total = fields.Float(string='Total', compute='_compute_total', store=True)

    @api.depends('price', 'quantity')
    def _compute_total(self):
        for wizard in self:
            wizard.total = wizard.price * wizard.quantity

    def open_car_wizard(self):
        self.ensure_one()  # Ensures only one record is selected
        return {
            'type': 'ir.actions.act_window',
            'name': 'Car Wizard',
            'res_model': 'car.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_name': self.name,
                'default_price': self.price,
                'default_quantity': self.quantity,
            }
        }
