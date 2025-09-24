from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    custom_char = fields.Char(string="Name")
    custom_bool = fields.Boolean(string="Active")
    custom_date = fields.Date(string="Date Available")
    custom_float = fields.Float(string="Range", digits=(6,2))
    enable_feature = fields.Boolean(string="My Features", config_parameter='car.enable_feature')
    custom_message = fields.Char(string="Model Name", config_parameter='car.custom_message')
    custom_reports =fields.Integer(string='No.Reports:')
    mark = fields.Text(string='Marks')
    custom_selection = fields.Selection([
        ('option_1', 'Option 1'),
        ('option_2', 'Option 2'),
        ('option_3', 'Option 3')
    ], string="Select Option")

    # Optional: Save settings in ir.config_parameter for persistence
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        IrConfigParam = self.env['ir.config_parameter'].sudo()
        res.update(
            custom_char=IrConfigParam.get_param('company.custom_char', default=''),
            custom_bool=IrConfigParam.get_param('company.custom_bool', default='False') == 'True',
            custom_date=IrConfigParam.get_param('company.custom_date', default=False),
            custom_float=float(IrConfigParam.get_param('company.custom_float', default=0.0)),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        IrConfigParam = self.env['ir.config_parameter'].sudo()
        IrConfigParam.set_param('company.custom_char', self.custom_char or '')
        IrConfigParam.set_param('company.custom_bool', str(self.custom_bool))
        IrConfigParam.set_param('company.custom_date', self.custom_date or '')
        IrConfigParam.set_param('company.custom_float', str(self.custom_float))
