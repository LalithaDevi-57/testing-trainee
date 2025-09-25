from odoo import models, fields, api

class MobileConsumerBillWizard(models.TransientModel):
    _name = 'mobile.consumer.bill.wizard'
    _description = 'Wizard to Create Mobile Consumer Bill'

    mobile_id = fields.Many2one('mobile.model', string='Mobile Model', required=True)
    product_id = fields.Many2one('product.master.data', string='Product', required=True)
    quantity = fields.Integer(string='Quantity', default=1)
    price = fields.Float(string='Price')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price = self.product_id.price

    def action_create_bill(self):
        self.ensure_one()
        self.env['mobile.consumer.bill'].create({
            'mobile_id': self.mobile_id.id,
            'product_id': self.product_id.id,
            'quantity': self.quantity,
            'price': self.price,
            'state': 'confirmed',
        })
        return {'type': 'ir.actions.act_window_close'}
