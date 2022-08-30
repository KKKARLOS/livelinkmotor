from odoo import api, models


class ReportPackaging(models.AbstractModel):
    _name = 'report.gst_lvl_packaging.report_label_report_packaging_new'
    _description = 'Generate label for the packaging in the stock picking outs'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('gst_lvl_packaging.report_label_report_packaging_new')
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self,
        }
        return docargs
