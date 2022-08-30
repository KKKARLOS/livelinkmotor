from odoo import api, models


class ReportStockProductionLot(models.AbstractModel):
    _name = 'report.gst_lvl_reports.report_label_qr_fabrication_lot'
    _description = 'generate label with qr codes representing the imei or the ' \
                   'mac as appropriate to the device in question'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('gst_lvl_reports.report_label_qr_fabrication_lot')
        docargs = {
            'doc_paperformat': self.env.ref('gst_lvl_reports.paperformat_livelink_label_qr_imei_mac_picking'),
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self,
        }
        return docargs
