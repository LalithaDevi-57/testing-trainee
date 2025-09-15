from odoo import models, fields,api
from datetime import timedelta

class OfficeAsset(models.Model):
    _name = "office.asset"
    _description = "Office Asset"

    name = fields.Char(string="Asset Name", required=True)
    asset_type = fields.Selection([
        ('furniture', 'Furniture'),
        ('electronics', 'Electronics'),
        ('software', 'Software'),
        ('other', 'Other'),
    ], string="Asset Type", default="other")
    purchase_date = fields.Date(string="Purchase Date")
    value = fields.Float(string="Asset Value")