from datetime import datetime, date, timedelta

from odoo import api, fields, models, _


class LvlStockMove(models.Model):
    _inherit = 'stock.move'


class LvlStockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def _get_sale_order(self):
        self.ensure_one()
        select = self._select_get_sale_order()
        self.env.cr.execute(select)
        return self.env.cr.dictfetchall()

    def _select_get_sale_order(self):
        return """
            SELECT s.id
            FROM stock_move_line l, stock_move m,
                procurement_group g, sale_order s
            WHERE m.id = l.move_id AND g.id = m.group_id
                AND s.id = g.sale_id
                AND lot_id = {0}
            LIMIT 1;
        """.format(self.lot_id.id)

    def _get_last_sale_order(self):
        self.ensure_one()
        select = self._select_get_last_sale_order()
        self.env.cr.execute(select)
        return self.env.cr.dictfetchall()

    def _select_get_last_sale_order(self):
        return """
            SELECT s.id, *
            FROM stock_move_line l, stock_production_lot t,
                stock_move m, procurement_group g, sale_order s
            WHERE l.lot_id = t.id
                AND m.id = l.move_id AND g.id = m.group_id
                AND s.id = g.sale_id
                AND t.name = '{0}' --'FMU02611'
                AND l.company_id = 1 -- ToDo: You can do it better
            LIMIT 1
        """.format(self.lot_id.name)
