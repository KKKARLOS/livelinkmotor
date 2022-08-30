from odoo import api, models


class ReportStockPackagingAndQR(models.AbstractModel):
    _name = 'report.gst_lvl_packaging.report_sotck_packaging_and_qr_new'
    _description = ''

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']
        report_name = \
            'gst_lvl_packaging.report_label_report_stock_packaging_and_qr_new'
        report = report_obj._get_report_from_name(report_name)
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self,
        }
        return docargs
