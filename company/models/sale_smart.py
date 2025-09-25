from odoo import models, fields,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_markup_percent = fields.Float(string='Markup %')

    def action_apply_markup(self):
        for order in self:
            for line in order.order_line:
                cost = line.product_id.standard_price
                markup = order.x_markup_percent or 0
                line.price_unit = cost * (1 + markup / 100)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Markup applied to all lines!',
                'type': 'success',
                'sticky': False,
            }
        }

    total_adjusted_price = fields.Monetary(
        string="Adjusted Total", compute="_compute_adjusted_price", currency_field="currency_id")

    def _compute_adjusted_price(self):
        for order in self:
            order.total_adjusted_price = sum(order.order_line.mapped('price_subtotal'))

    def action_view_adjusted_lines(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Adjusted Order Lines',
            'res_model': 'sale.order.line',
            'view_mode': 'tree,form',
            'domain': [('order_id', '=', self.id)],
            'context': {'default_order_id': self.id},
        }



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id', 'order_id', 'product_uom_qty')
    def _onchange_product_id_markup(self):
        if self.product_id and self.order_id:
            cost = self.product_id.standard_price
            markup = self.order_id.x_markup_percent or 0
            self.price_unit = cost * (1 + markup / 100)

    @api.onchange('product_id', 'order_id.x_markup_percent')
    def _onchange_price_with_markup(self):
        for line in self:
            if line.product_id and line.order_id.x_markup_percent:
                base_price = line.product_id.lst_price or 0.0
                markup = line.order_id.x_markup_percent
                line.price_unit = base_price * (1 + markup / 100)


