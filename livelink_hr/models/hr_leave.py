from datetime import datetime, date, timedelta

from odoo import api, fields, models, _


class LvlHrLeave(models.Model):
    _inherit = 'hr.leave'

    @api.onchange('request_date_from', 'request_date_to', 'number_of_days')
    def _onchange_update_days(self):
        if self.request_date_from and self.request_date_to \
                and self.state not in ['validate', 'validate1']:
            diff = self.request_date_to - self.request_date_from
            non_wd = sum([True for days in range(diff.days) if (self.request_date_from + timedelta(days=days)).weekday() > 4])
            self.number_of_days = diff.days - non_wd + 1
