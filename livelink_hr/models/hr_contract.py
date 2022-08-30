from datetime import datetime, date, timedelta

from odoo import api, fields, models, _


class LvlHrContract(models.Model):
    _inherit = 'hr.contract'

    year = datetime.now().year
    fix = 22
    ini = date(year, 1, 1)
    fin = date(year, 12, 31)
    dtini = datetime(year, 1, 1, 0,0,0)

    @api.model
    def create(self, vals):
        rec_cont = super(LvlHrContract, self).create(vals)
        if 'date_end' in vals or 'trial_date_end' in vals \
                or 'date_start' in vals:
            rec_cont.create_leave_allocation()
        return rec_cont

    def write(self, vals):
        rec_cont = super(LvlHrContract, self).write(vals)
        if 'date_end' in vals or 'trial_date_end' in vals \
                or 'date_start' in vals or self.date_end \
                    or self.date_start or self.trial_date_end:
            self.create_leave_allocation()
        return rec_cont

    def action_holidays_generator(self):
        args = [('state', '=', 'open')]
        self.search(args).create_leave_allocation()

    def _get_prorate_by_day(self):
        return round(self.fix/365, 4)

    def _get_accrued_holidays(self, contract):
        ini0 = self.ini
        if self.ini < contract.date_start: ini0 = contract.date_start
        fin0 = False
        if contract.trial_date_end: fin0 = contract.trial_date_end
        if contract.date_end:
            if not fin0 or fin0 < contract.date_end: fin0 = contract.date_end
        if not fin0: fin0 = self.fin
        work_days = (fin0 - ini0).days + 1
        ratio = self._get_prorate_by_day()
        return int(work_days * ratio)

    def create_leave_allocation(self):
        obj_all = self.env['hr.leave.allocation']
        lempl = []
        for contract in self:
            e = contract.employee_id
            days = self._get_accrued_holidays(contract)
            vals = self.get_hr_leave_allocation(e, days)
            if vals: lempl.append(vals)
        rec_ids = obj_all.create(lempl)
        rec_ids.action_approve()

    def get_hr_leave_allocation(self, employee, days):
        rec_type = self.env.ref('livelink_hr.hr_leave_type_holidays')
        vals = {}
        if rec_type:
            obj_all = self.env['hr.leave.allocation']
            args = [('employee_id', '=', employee.id),
                    ('holiday_status_id', '=', rec_type.id),
                    ('write_date', '>', self.dtini)]
            rec_all = obj_all.search(args, order='id desc')
            if rec_all:
                current = rec_all[0]
                days -= sum((rec_all - current).mapped('number_of_days'))
                if days < 0: days = 0
                current.write({'number_of_days': days})
            else:
                vals.update({
                    'name': rec_type.name,
                    'holiday_status_id': rec_type.id,
                    'allocation_type': 'regular',
                    'number_of_days': days,
                    'holiday_type': 'employee',
                    'employee_id': employee.id,
                })
        return vals
        