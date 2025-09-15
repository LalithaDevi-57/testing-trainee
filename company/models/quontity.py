from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    total_qty = fields.Float(
        string="Total Q",
        compute="_compute_total_qty",
        store=True,
        tracking=True
    )

    @api.depends('move_ids_without_package.product_uom_qty')
    def _compute_total_qty(self):
        for rec in self:
            rec.total_qty = sum(line.product_uom_qty for line in rec.move_ids_without_package)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    total_qty = fields.Float(
        string="Total Q",
        compute="_compute_total_qty",
        store=True,
        tracking=True
    )

    @api.depends('order_line.product_qty')
    def _compute_total_qty(self):
        for rec in self:
            rec.total_qty = sum(line.product_qty for line in rec.order_line)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_qty = fields.Float(
        string="Total Q",
        compute="_compute_total_qty",
        store=True,
        tracking=True
    )

    @api.depends('order_line.product_uom_qty')
    def _compute_total_qty(self):
        for rec in self:
            rec.total_qty = sum(line.product_uom_qty for line in rec.order_line)