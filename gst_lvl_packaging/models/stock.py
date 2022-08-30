from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    is_autogenerated = fields.Boolean(string='Bot register?', default=False)
    workorder_id = fields.Many2one(
        comodel_name='mrp.workorder',
        string='Cached workorder',
    )

#    origin_sml_serial = fields.Many2many('stock.production.lot',
#            string='Lotes consumidos')

    consumed_imei = fields.Many2one('aws.device', string='Consumed device')
    consumed_key = fields.Many2one('aws.key', string='Consumed key')

    def _set_production_traceability(self):
        lots = self._get_main_serial()
        return lots

    def _get_main_serial(self, sml_ids=False):
        objSML = self.env['stock.move.line']
        if not sml_ids:
            args = [('lot_id', 'in', self.ids),
                    ('consume_line_ids', '!=', False)]
        else: args = [('lot_id', '!=', False), ('id', 'in', sml_ids)]
        
        recSML = objSML.search(args)
        lots = recSML.mapped('lot_id')
        if recSML:
            lots |= lots._get_main_serial(recSML.mapped('consume_line_ids.id'))
        lots |= self
        return lots
            
    def _set_assign_serial(self, recLot):
        cids = self.env['res.company'].sudo().search([]).ids
        sself = self.with_context(allowed_company_ids=cids)
        
        lot_names = recLot.mapped('name')
        argsD = [('device_id.name', 'in', lot_names)] #, ('is_device', '=', True)]
        argsK = [('key_id.name', 'in', lot_names)] #, ('is_mac', '=', True)]
        recImei = sself.search(argsD, limit=1, order='id desc')
        if recImei: sself.consumed_imei = recImei.device_id.id
        recKey = sself.search(argsK, limit=1, order='id desc')
        if recKey: sself.consumed_key = recKey.key_id.id

    def _set_production_traceability1(self):
        for recLot in self:
            rec_smlp = recLot._get_stock_move_line_production()
            for c in rec_smlp.consume_line_ids:
                if c.lot_id:
                    if c.lot_id.device_id and (not recLot.consumed_imei \
                            or not recLot.origin_sml_imei):
                        recLot.consumed_imei = c.lot_id.device_id
                        recLot.origin_sml_imei = c
                    if c.lot_id.key_id and (not recLot.consumed_key \
                            or not recLot.origin_sml_key):
                        recLot.consumed_key = c.lot_id.key_id
                        recLot.origin_sml_key = c  

    def _get_stock_move_line_production(self):
        self.ensure_one()
        if self.origin_sml_serial:
            rec_move_line = self.origin_sml_serial
        else:
            rec_move_line = self._get_record_stock_move_line()
            if rec_move_line: self.origin_sml_serial = rec_move_line
        return rec_move_line

    def _get_record_stock_move_line(self):
        sql_query = self._get_query_search_stock_move_line_production()
        self._cr.execute(sql_query)
        sml_ids = [res[0] for res in self._cr.fetchall()]
        return self.env['stock.move.line'].browse(sml_ids)

    def _get_query_search_mrp_production(self):
        # Obtener Orden de Producción de un Serial
        return '''
            SELECT m.production_id
            FROM stock_move m, stock_move_line l,
                stock_production_lot t
            WHERE l.move_id = m.id AND l.lot_id = t.id
                AND l.lot_id = {0}
                AND m.production_id is not NULL        
        '''.format(self.id)

    def _get_query_search_stock_move_line_production(self):
        return '''
            SELECT l.id
            FROM stock_move m, stock_move_line l,
                stock_production_lot t
            WHERE l.move_id = m.id AND l.lot_id = t.id
                AND l.lot_id = {0}
                AND m.production_id is not NULL
        '''.format(self.id)

    def show_rieju_report(self):
        #self._set_production_traceability()
        report = 'gst_lvl_packaging.report_label_rieju'
        return self.env.ref(report).report_action(self)