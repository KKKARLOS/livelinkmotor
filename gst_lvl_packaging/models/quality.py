from odoo import _, api, models, fields


class QualityCheck(models.Model):
    _inherit = "quality.check"

    def button_print_rieju(self):
        return self.finished_lot_id.show_rieju_report()

    def button_print_serial_number_finished(self):
        self.ensure_one()
        report = 'gst_lvl_packaging.' \
                 'report_label_serial_number_again'
        return self.env.ref(report).report_action(self)

    def button_print_qr_finished(self): # WO / Pasos varios / Button Codigo QR
        self.ensure_one()
        report = 'gst_lvl_packaging.' \
                 'report_label_qr_again'
        return self.env.ref(report).report_action(self)

    def button_print_label(self): # WO / Pasos varios / Button Codigo Barras
        self.ensure_one()
        report = 'gst_lvl_packaging.report_label_report_packaging_again'
        print(self.get_imei())
        return self.env.ref(report).report_action(self)

    def get_imei(self):
        args = [('finished_lot_id.name', '=', self.finished_lot_id.name),
                ('lot_id.is_device', '=', True)]
        rec_dev = self.env['quality.check'].search(args, limit=1)
        return rec_dev.lot_id.name if rec_dev else ""

    def get_mac(self):
        args = [('finished_lot_id.name', '=', self.finished_lot_id.name),
                ('lot_id.is_mac', '=', True)]
        rec_mac = self.env['quality.check'].search(args, limit=1)
        return rec_mac.lot_id.name if rec_mac else ""

    def get_imei_mac_qr_format(self):
        qr_format = ""
        imei = self.get_imei()
        mac = self.get_mac()

        if imei != "" and mac == "": qr_format = imei + ";"
        elif mac != "" and imei == "": qr_format = ";" + mac
        elif imei != "" and mac != "": qr_format = imei + ";" + mac

        if self.workorder_id.is_rieju: qr_format = self.finished_lot_id.name

        return qr_format

