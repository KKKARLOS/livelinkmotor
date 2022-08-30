from odoo import _, api, models, fields


def print_serial_number(self):
    sn = self
    self.ensure_one()
    report = 'gst_lvl_packaging.' \
             'report_label_serial_number'
    return self.env.ref(report).report_action(self)


def print_qr(self):
    self.ensure_one()
    report = 'gst_lvl_packaging.' \
             'report_label_qr_fabrication_lot_imei_plus_mac_new'
    return self.env.ref(report).report_action(self)
