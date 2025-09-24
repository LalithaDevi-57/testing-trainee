from odoo import models
import base64

class ReportCarModel(models.AbstractModel):
    _name = 'report.car.car_model_report_template'

    def _get_report_values(self, docids, data=None):
        docs = self.env['car.model'].browse(docids)
        with open('/path/to/invoice.png', 'rb') as image_file:
            watermark_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        return {
            'docs': docs,
            'your_base64_variable': watermark_base64,
        }