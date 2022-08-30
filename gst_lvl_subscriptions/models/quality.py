from odoo import _, api, models, fields


class QualityCheck(models.Model):
    _inherit = "quality.check"

    def getImei(self):
        qualitiesAux = self.env['quality.check'].search_read([['finished_lot_id.name', '=', self.finished_lot_id.name]])
        imei = ""
        for quality in qualitiesAux:
            if 'DEV' in quality['component_id'][1]:
                imei = quality['lot_id'][1]
        return imei

    def getMac(self):
        qualitiesAux = self.env['quality.check'].search_read([['finished_lot_id.name', '=', self.finished_lot_id.name]])
        mac = ""
        for quality in qualitiesAux:
            if 'KEY' in quality['component_id'][1]:
                mac = quality['lot_id'][1]
        return mac
