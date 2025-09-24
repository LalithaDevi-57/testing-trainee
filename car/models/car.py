from reportlab.lib.validators import inherit

from odoo import models, fields, api
from odoo.exceptions import UserError

class CarModel(models.Model):
    _name = 'car.model'
    _description = 'Car Model'


    name = fields.Char(string='Car Name', required=True)
    brand = fields.Char(string='Brand')
    model_year = fields.Integer(string='Model Year')
    price = fields.Float(string='Price')
    car_id=fields.Many2one('garage.car','Car Id')
    description = fields.Text(string='Description')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    line_ids = fields.One2many('car.line', 'car_id', string='Car Lines')
    is_locked = fields.Boolean(string="Is Locked", default=False)
    quantity = fields.Integer(string='Quantity')
    sequence_no = fields.Char(string='Sequence Number', required=True, copy=False, readonly=True, default='New')
    state = fields.Selection([('fill', 'Fill'), ('done', 'Done')], string='Status')
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.company.currency_id.id,
    )
    total_amount = fields.Monetary(
        string='Total Amount',
        compute='_compute_total_amount',
        store=True,
        currency_field='currency_id'
    )

    @api.onchange('name')
    def onchange_name(self):
        if self.name == 'honda':
            self.price = 1200000.00
            self.model_year= 2024
            self.brand='RT'
        else:
            self.price = 0.0
            self.model_year=0-0

    # dynamically
    def create_garage_car(self):
        for record in self:
            self.env['garage.car'].create({
                'name': record.name + ' Copy',
                'brand': record.brand,
                'model_year': record.model_year,
                'partner_id': record.partner_id.id,
            })
    # static
    # def create_garage_car(self):
    #     for record in self:
    #         self.env['garage.car'].create({
    #             'name': 'Priya',
    #             'brand': 'Pink',
    #             'model_year': 2002,
    #             'partner_id': 1,
    #         })
    # def delete_car(self):
    #     car = self.env['garage.car'].browse(2)
    #     if car.exists():
    #         car.unlink()
    #         return "Car deleted."
    #     return "Car not found."
    #
    # def delete_car(self):
    #     cars = self.env['car.model'].browse([32, 35])
    #     if cars.exists():
    #         cars.unlink()
    #         return "10 cars deleted."
    #     else:
    #         return "No cars found."

    def delete_car(self):
        ids_to_delete = list(range(28, 34))  # IDs from 1 to 100
        cars = self.env['car.model'].browse(ids_to_delete)
        if cars.exists():
            cars.unlink()
            return f"{len(ids_to_delete)} cars deleted."
        else:
            return "No cars found."

    @api.depends('line_ids.total')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.line_ids.mapped('total'))

    def get_all_car_names(self):
        cars = self.env['garage.car'].search([])
        return cars.mapped('name')

    def action_fill(self):
        for rec in self:
            rec.state = 'fill'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def write(self, vals):
        result = super(CarModel, self).write(vals)
        for record in self:
            if record.state == 'fill':
                record.state = 'done'
        return result

    def import_master_data_lines(self):
        for record in self:
            master_records = self.env['master.data'].search([])
            lines = []
            for product in master_records:
                lines.append((0, 0, {
                    'product_name': product.name,
                    'quantity': product.quantity,
                    'price': product.price,
                }))
            record.line_ids = lines

    @api.model
    def create(self, vals):
        if vals.get('sequence_no', 'New') == 'New':
            vals['sequence_no'] = self.env['ir.sequence'].next_by_code('car.line.sequence') or 'New'
        return super().create(vals)

    # @api.model
    # def create(self, vals):
    #     # print(f"Before sequence update: {vals}")
    #     if vals.get('sequence_no', 'New') == 'New':
    #         vals['sequence_no'] = self.env['ir.sequence'].next_by_code('car.line.sequence') or 'New'
    #         # print(f"After sequence update: {vals}")
    #     return super().create(vals)

    def lock_and_archive(self):
        for record in self:
            record.is_locked = True

            # Create archived record
            archived = self.env['archived.car.model'].create({
                'name': record.name,
                'brand': record.brand,
                'model_year': record.model_year,
                'price': record.price,
                'description': record.description,
                'source_car_id': record.id,
                'currency_id': record.currency_id.id,
                'total_amount': record.total_amount,
                'sequence_no': record.sequence_no,
            })

            # Copy lines
            for line in record.line_ids:
                self.env['archived.car.line'].create({
                    'archived_car_id': archived.id,
                    'product_name': line.product_name,
                    'quantity': line.quantity,
                    'price': line.price,
                })

        # Open the archived record form view
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'archived.car.model',
            'view_mode': 'form',
            'res_id': archived.id,
            'target': 'current',
        }

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

    @api.model
    def delete_done_cars(self):
        # Search for records where state = 'done'
        done_cars = self.env['car.model'].search([('state', '=', 'done')])
        if done_cars:
            done_cars.unlink()
            return f"Deleted {len(done_cars)} 'done' state cars."
        return "No cars with state 'done' found."


class CarLine(models.Model):
    _name = 'car.line'
    _description = 'Car Line'

    car_id = fields.Many2one('car.model', string='Car', ondelete='cascade', required=True)
    product_name = fields.Char(string='Product Name', required=True)
    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    price = fields.Float(string='Unit Price', required=True)

    currency_id = fields.Many2one(
        related='car_id.currency_id',
        store=True,
        string='Currency',
        readonly=True
    )

    total = fields.Monetary(
        string='Total',
        compute='_compute_total',
        store=True,
        currency_field='currency_id'
    )

    @api.depends('quantity', 'price')
    def _compute_total(self):
        for line in self:
            line.total = line.quantity * line.price


class MasterData(models.Model):
    _name = 'master.data'
    _description = 'Product Master Data'

    name = fields.Char(string='Product Name', required=True)
    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    price = fields.Float(string='Unit Price', required=True)
    total = fields.Float(string='Total', compute='_compute_total', store=True)

    @api.depends('quantity', 'price')
    def _compute_total(self):
        for line in self:
            line.total = line.quantity * line.price


class ArchivedCarModel(models.Model):
    _name = 'archived.car.model'
    _description = 'Archived Car Model'

    name = fields.Char(string='Car Name')
    brand = fields.Char(string='Brand')
    model_year = fields.Integer(string='Model Year')
    price = fields.Float(string='Price')
    description = fields.Text(string='Description')
    source_car_id = fields.Many2one('car.model', string='Source Car')
    sequence_no = fields.Char(string='Sequence Number', required=True, copy=False, readonly=True, default='New')

    @api.model
    def create(self, vals):
        if vals.get('sequence_no', 'New') == 'New':
            vals['sequence_no'] = self.env['ir.sequence'].next_by_code('car.line.sequence') or 'New'
        return super().create(vals)

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.company.currency_id.id
    )
    total_amount = fields.Monetary(
        string='Total Amount',
        compute='_compute_total_amount',
        store=True,
        currency_field='currency_id'
    )

    @api.depends('line_ids.total')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.line_ids.mapped('total'))

    line_ids = fields.One2many('archived.car.line', 'archived_car_id', string='Archived Car Lines')


class ArchivedCarLine(models.Model):
    _name = 'archived.car.line'
    _description = 'Archived Car Line'

    archived_car_id = fields.Many2one('archived.car.model', string='Archived Car', ondelete='cascade')
    product_name = fields.Char(string='Product Name')
    quantity = fields.Float(string='Quantity')
    price = fields.Float(string='Unit Price')

    currency_id = fields.Many2one(
        related='archived_car_id.currency_id',
        store=True,
        string='Currency',
        readonly=True
    )

    total = fields.Monetary(
        string='Total',
        compute='_compute_total',
        store=True,
        currency_field='currency_id'
    )

    @api.depends('quantity', 'price')
    def _compute_total(self):
        for line in self:
            line.total = line.quantity * line.price


class CarReport(models.AbstractModel):
    _name = 'report.car.car_report_template1'
    _description = 'Car Model Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['car.model'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'car.model',
            'docs': docs,
        }


class Payments(models.Model):
    _inherit ='account.move'

    state = fields.Selection([('draft','Draft'),
            ('approved_one', 'Approved 1'),
            ('approved_two', 'Approved 2'),('posted','posted'),('cancel','Cancelled')
        ],
        ondelete={
            'approved_one': 'set default',
            'approved_two': 'set default',
        },
    )
class PaymentButton(models.Model):
    _inherit ='account.payment'


    def action_approve_one(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'approved_one'

    def action_draft_nhcl(self):
        for rec in self:
            if rec.state == 'approved_one':
                rec.state = 'approved_two'

    def action_post_final(self):
        for rec in self:
            if rec.state == 'approved_two':
                rec.state = 'posted'
class Car(models.Model):
    _name = 'car.care'
    _description = 'Car Model'

    name = fields.Char(string='Car Name')
    def create_product(self):
        product_vals = {
            'name': 'My Custom Product',
            'default_code': 'MY_PROD_001',
            'list_price': 150.0,
            'standard_price': 100.0,
            'type': 'product',
            'uom_id': self.env.ref('uom.product_uom_unit').id,
            'uom_po_id': self.env.ref('uom.product_uom_unit').id,
            'categ_id': self.env.ref('product.product_category_all').id,
        }
        new_product = self.env['product.template'].create(product_vals)
        return new_product

    def create_multiple_products(self):
        product_data = [
            {
                'name': 'Product A',
                'default_code': 'PROD_A',
                'list_price': 100.0,
                'standard_price': 60.0,
            },
            {
                'name': 'Product B',
                'default_code': 'PROD_B',
                'list_price': 120.0,
                'standard_price': 70.0,
            },
            {
                'name': 'Product C',
                'default_code': 'PROD_C',
                'list_price': 140.0,
                'standard_price': 80.0,
            },
        ]

        products = []
        for vals in product_data:
            vals.update({
                'type': 'product',
                'uom_id': self.env.ref('uom.product_uom_unit').id,
                'uom_po_id': self.env.ref('uom.product_uom_unit').id,
                'categ_id': self.env.ref('product.product_category_all').id,
            })
            product = self.env['product.template'].create(vals)
            products.append(product)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Created Products',
            'res_model': 'product.template',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', [p.id for p in products])],
        }

    def create_contact(self):
        contact_vals = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '+1234567890',
            'company_type': 'person',
            'is_company': False,
        }
        contact = self.env['res.partner'].create(contact_vals)
        return contact

    def create_multiple_contacts(self):
        contacts_data = [
            {'name': 'Contact A', 'email': 'contacta@example.com', 'phone': '1234567890'},
            {'name': 'Contact B', 'email': 'contactb@example.com', 'phone': '0987654321'},
            {'name': 'Contact C', 'email': 'contactc@example.com', 'phone': '5555555555'},
        ]

        created_contacts = []
        for data in contacts_data:
            contact = self.env['res.partner'].create(data)
            created_contacts.append(contact)

        return created_contacts

    def create_new_user(self):
        user_vals = {
            'name': 'Sneha',
            'login': 'sneha@gmail.com',
            'email': 'sneha@egmail.com',
            'password': 'admin',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])],
        }
        new_user = self.env['res.users'].create(user_vals)
        return new_user
