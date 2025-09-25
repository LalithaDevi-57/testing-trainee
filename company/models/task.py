from odoo import models, fields,api,_
from odoo.exceptions import UserError

class OfficeTask(models.Model):
    _name = "office.task"
    _description = "Office Task"

    name = fields.Char(string="Task Name", required=True)
    project_id = fields.Many2one("office.project", string="Project")
    assigned_to = fields.Many2one("office.employee", string="Assigned To")
    deadline = fields.Date(string="Deadline")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ], string="Status", default="draft")

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    state = fields.Selection(
        selection_add=[('approved', 'Approved'), ('purchase',)],
        ondelete={"approved": "set default"},
    )
    approved = fields.Boolean(string="Approved", default=False)

    @api.depends("amount_total", "approved")
    def _compute_show_approve_button(self):
        for order in self:
            order.show_approve_button = order.amount_total >= 5000 and not order.approved

    def action_approve(self):
        for order in self:
            if order.amount_total >= 5000 and not order.approved:
                order.approved = True
                order.write({"state": "approved"})
                order.message_post(body="Purchase Order has been approved.")

    show_approve_button = fields.Boolean(
        string="Show Approve Button",

        compute="_compute_buttons"
    )
    show_confirm_button = fields.Boolean(
        string="Show Confirm Button",
        compute="_compute_buttons"
    )

    @api.depends("amount_total", "approved", "state")
    def _compute_buttons(self):
        for order in self:
            if order.state in ("purchase",):
                order.show_approve_button = False
                order.show_confirm_button = False
            else:
                if order.amount_total >= 5000:
                    if not order.approved:
                        order.show_approve_button = True
                        order.show_confirm_button = False
                    else:
                        order.show_approve_button = False
                        order.show_confirm_button = True
                else:
                    order.show_approve_button = False
                    order.show_confirm_button = True

    def button_confirm(self):
        for order in self:
            if order.amount_total >= 5000 and not order.approved:
                raise UserError(_("This Purchase Order must be approved before confirmation."))
            if order.state == "approved":
                order.state = "purchase"
        return super().button_confirm()


# #
#     approved_button_visible = fields.Boolean(
#         compute="_compute_approved_button_visible",
#         string="Approved Button Visible"
#     )
#
#     @api.depends('amount_total')
#     def _compute_approved_button_visible(self):
#         for order in self:
#             order.approved_button_visible = order.amount_total > 5000
#
#     def action_approve_po(self):
#      for order in self:
#         order.state = 'approved' # Or create a new state if needed
#
#     def action_approve(self):
#         for order in self:
#             if order.amount_total >= 5000 and not order.approved:
#                 order.approved = True
#                 order.write({"state": "approved"})
#                 order.message_post(body="Purchase Order has been approved.")





