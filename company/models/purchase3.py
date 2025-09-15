from odoo import models, fields, api
from odoo.exceptions import UserError

class CompanyPurchase(models.Model):
    _name = 'company.purchase'
    _description = 'Custom Purchase Order'

    name = fields.Char(string="Reference", required=True, default="New")
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True)
    date_order = fields.Datetime(string='Order Date', default=fields.Datetime.now)
    line_ids = fields.One2many('company.purchase.line', 'order_id', string='Order Lines')
    real_purchase_order_id = fields.Many2one('purchase.order', string='Real Purchase Order', readonly=True)

    def action_create_real(self):
        """This method creates a real purchase.order"""
        PurchaseOrder = self.env['purchase.order']
        PurchaseOrderLine = self.env['purchase.order.line']

        for rec in self:
            if rec.real_purchase_order_id:
                raise UserError("Purchase Order already created.")

            po = PurchaseOrder.create({
                'partner_id': rec.partner_id.id,
                'date_order': rec.date_order,
                'order_line': [
                    (0, 0, {
                        'product_id': line.product_id.id,
                        'name': line.name,
                        'product_qty': line.quantity,
                        'price_unit': line.price_unit,
                        'date_planned': fields.Datetime.now(),

                    }) for line in rec.line_ids
                ]
            })
            rec.real_purchase_order_id = po.id

class CompanyPurchaseLine(models.Model):
    _name = 'company.purchase.line'
    _description = 'Custom Purchase Order Line'

    order_id = fields.Many2one('company.purchase', string='Custom Order Reference', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    name = fields.Char(string='Description')
    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price')


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for order in self:
            existing = self.env['company.purchase'].search([('name', '=', order.name)], limit=1)
            if not existing:
                self.env['company.purchase'].create({
                    'name': order.name,
                    'partner_id': order.partner_id.id,
                    'date_order': order.date_order,
                    'line_ids': [(0, 0, {
                        'product_id': line.product_id.id,
                        'quantity': line.product_qty,
                        'price_unit': line.price_unit,
                        'name': line.name,
                    }) for line in order.order_line]
                })
        return res

    @api.model
    def create(self, vals):
        partner = self.env['res.partner'].browse(vals.get('partner_id'))
        sequence = self.env['ir.sequence'].next_by_code('purchase.order') or '/'
        if partner:
            vals['name'] = f"{sequence} - {partner.name}"
        return super(PurchaseOrder, self).create(vals)

