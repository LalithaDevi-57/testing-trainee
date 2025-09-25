
from odoo import models, fields, api
from num2words import num2words



class AccountMove(models.Model):
    _inherit = 'account.move'


    amount_in_words = fields.Char(string='Amount in Words', compute='_compute_amount_in_words', store=True)

    @api.depends('partner_id')
    def _compute_place_of_supply(self):
        for rec in self:
            rec.place_of_supply = rec.partner_id.state_id.id if rec.partner_id.state_id else False


    @api.depends('amount_total', 'currency_id')
    def _compute_amount_in_words(self):
        for rec in self:
            if rec.amount_total and rec.currency_id:
                try:
                    words = num2words(rec.amount_total, lang='en_IN')
                except:
                    words = num2words(rec.amount_total, lang='en')
                rec.amount_in_words = f"{words} {rec.currency_id.currency_unit_label or rec.currency_id.name}"
            else:
                rec.amount_in_words = ''