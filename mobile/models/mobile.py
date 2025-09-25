from odoo import models, fields, api
from odoo.exceptions import UserError,ValidationError


class MobileModel(models.Model):
    _name = 'mobile.model'
    _description = 'Mobile Phone Model'

    name = fields.Char(string='Mobile Model Name', required=True)
    brand = fields.Char(string='Brand')
    release_date = fields.Date(string='Release Date')
    description=fields.Char(string='Description')
    today_date=fields.Date(string='Today Date')
    bill_ids = fields.One2many('mobile.consumer.bill', 'mobile_id', string='Consumer Bills')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    product_id = fields.Many2one('product.master.data', string='Product')


    state = fields.Selection([
        ('fill', 'Fill'),
        ('done', 'Done'),
    ], string='Status', tracking=True)

    def action_mark(self):
        for record in self:
            record.state = 'fill'

    sequence_no = fields.Char(string='Bill Number', required=True, copy=False, readonly=True, default='New')

    @api.depends('bill_ids.total')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(bill.total for bill in record.bill_ids)

    @api.model
    def create(self, vals):
        if vals.get('sequence_no', 'New') == 'New':
            vals['sequence_no'] = self.env['ir.sequence'].next_by_code('mobile.model') or 'New'
            vals['state'] = 'done'

        return super(MobileModel, self).create(vals)

    def write(self, vals):
        result = super(MobileModel, self).write(vals)
        for record in self:
            if record.state == 'fill':
                record.state = 'done'
        return result

    product_line_ids = fields.One2many('mobile.product.line', 'mobile_id', string='Product Lines')

    def action_load_products(self):
        """Button action: Load all products from master and create child lines automatically."""
        # Fetch all master products
        master_products = self.env['product.master.data'].search([])
        for rec in self:
            line_vals = []
            for product in master_products:
                line_vals.append((0, 0, {
                    'product_id': product.id,  # Product ID from master
                    'quantity': product.quantity,  # Quantity from master
                    'price': product.price,  # Price from master
                }))
            # Add all lines to the One2many field
            if line_vals:
                rec.write({'product_line_ids': line_vals})

    # def action_create_consumer_bill(self):
    #     for record in self:
    #         if record.state == 'fill':
    #             raise UserError("Cannot create a Consumer Bill in 'Done' state.")
    #         if not record.product_id:
    #             raise ValidationError("Please select a Product before creating a Consumer Bill.")
    #
    #         self.env['mobile.consumer.bill'].create({
    #             'mobile_id': record.id,
    #             'product_id': record.product_id.id,
    #             'quantity': 1,
    #             'price': record.product_id.price if record.product_id else 0.0,
    #         })
    #         record.state = 'done'
    def action_success(self):
        self.state = 'fill'
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mobile.consumer.bill.wizard',
            'view_mode': 'form',
            'target': 'new',
        }

    def action_copy_to_archive(self):
        for record in self:
            # Create the archive record
            archive = self.env['mobile.archive'].create({
                'name': record.name,
                'brand': record.brand,
                'release_date': record.release_date,
                'description': record.description,
                'total_amount': record.total_amount,
                'product_id': record.product_id.id if record.product_id else False,
                'sequence_no': record.sequence_no,
            })

            # Copy all product lines from mobile.product.line into mobile.archive.product.line
            for line in record.product_line_ids:
                self.env['mobile.archive.product.line'].create({
                    'archive_id': archive.id,
                    'product_id': line.product_id.id if line.product_id else False,
                    'quantity': line.quantity,
                    'price': line.price,
                    'total': line.total,
                    'state': 'confirmed',  # You can set default state
                })

            # Optional: Copy consumer bills if needed
            for bill in record.bill_ids:
                self.env['mobile.archive.product.line'].create({
                    'archive_id': archive.id,
                    'product_id': bill.product_id.id if bill.product_id else False,
                    'quantity': bill.quantity,
                    'price': bill.price,
                    'total': bill.total,
                    'state': bill.state,
                })

            # Open the archive form view
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'mobile.archive',
                'view_mode': 'form',
                'res_id': archive.id,
                'target': 'current',
            }


    @api.onchange('start_date', 'end_date')
    def _onchange_date_range(self):
        """Populate product lines with products released between start_date and end_date"""
        for rec in self:
            if rec.start_date and rec.end_date:
                # Search products within the date range
                master_products = self.env['product.master.data'].search([
                    ('release_date', '>=', rec.start_date),
                    ('release_date', '<=', rec.end_date),
                ])
                lines = []
                for product in master_products:
                    lines.append((0, 0, {
                        'product_id': product.id,
                        'quantity': product.quantity,
                        'price': product.price,
                    }))
                rec.product_line_ids = lines
            else:
                # Clear lines if dates are not set
                rec.product_line_ids = []
class MobileConsumerBill(models.Model):
    _name = 'mobile.consumer.bill'
    _description = 'Mobile Consumer Bill'

    mobile_id = fields.Many2one('mobile.model', string='Mobile Model', required=True, ondelete='cascade')
    quantity = fields.Integer(string='Quantity', default=1)
    price = fields.Float(string='Price')
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    product_id = fields.Many2one('product.master.data', string='Product', required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], default='draft', string='Status')


    @api.depends('quantity', 'price')
    def _compute_total(self):
        for record in self:
            record.total = record.quantity * record.price

class ProductMasterData(models.Model):
    _name = 'product.master.data'
    _description = 'Product Master Data'
    _rec_name = 'name'

    name = fields.Char(string='Product Name', required=True)
    quantity = fields.Integer(string='Quantity', required=True)
    price = fields.Float(string='Unit Price', required=True)
    release_date=fields.Date(string='Release Date')
    total = fields.Float(string='Total', compute='_compute_total', store=True)

    @api.depends('quantity', 'price')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.quantity * rec.price




class MobileProductLine(models.Model):
    _name = "mobile.product.line"
    _description = "Mobile Product Line"

    mobile_id = fields.Many2one("mobile.model", string="Mobile", ondelete="cascade")
    product_id = fields.Many2one("product.product", string="Product", required=True)
    quantity = fields.Integer(string="Quantity", default=1, required=True)
    price = fields.Float(string="Unit Price", required=True)
    total = fields.Float(string="Total", compute="_compute_total", store=True)

    @api.depends("quantity", "price")
    def _compute_total(self):
        for rec in self:
            rec.total = rec.quantity * rec.price




class MobileArchive(models.Model):
    _name = 'mobile.archive'
    _description = 'Archived Mobile Models'

    name = fields.Char(string='Mobile Model Name')
    brand = fields.Char(string='Brand')
    release_date = fields.Date(string='Release Date')
    description = fields.Text(string='Description')
    total_amount = fields.Float(string='Total Amount')
    product_id = fields.Many2one('product.master.data', string='Product')
    sequence_no = fields.Char(string='Bill Number')


    bill_ids = fields.One2many('mobile.archive.product.line', 'archive_id', string='Archived Bills')

class MobileArchiveProductLine(models.Model):
    _name = "mobile.archive.product.line"
    _description = "Archived Mobile Product Line"

    archive_id = fields.Many2one(
        "mobile.archive", string="Archive", ondelete="cascade", required=True
    )
    product_id = fields.Many2one("product.product", string="Product")
    quantity = fields.Integer(string="Quantity")
    price = fields.Float(string="Price")
    total = fields.Float(string="Total", compute="_compute_total", store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string='Status', default='confirmed')

    @api.depends("quantity", "price")
    def _compute_total(self):
        for rec in self:
            rec.total = rec.quantity * rec.price

# class ApprovalRequestInherit(models.Model):
#     _inherit = 'approval.request'
#
#     happy = fields.Char(string="Happy")
#
#
# class ApprovalRequestLineInherit(models.Model):
#     _inherit = 'approval.product.line'
#
#     happy = fields.Char(string="Happy")



