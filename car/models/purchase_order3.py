from odoo import models, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def update_padding(self):
        try:
            result = super(PurchaseOrder, self).update_padding()
            print("Called super method successfully")
        except AttributeError:
            print("No parent update_padding method to call")
            result = None
        sequence = self.env['ir.sequence'].search([('code', '=', 'purchase.order')], limit=1)
        if sequence:
            print(f"Before update: padding={sequence.padding}, next number={sequence.number_next}")
            sequence.padding = 6
            sequence.number_next = 1
            sequence._clear_cache()
            print(f"After update: padding={sequence.padding}, next number={sequence.number_next}")
            return "Padding updated successfully"
        else:
            print("Purchase order sequence not found")
            return "Purchase order sequence not found"
