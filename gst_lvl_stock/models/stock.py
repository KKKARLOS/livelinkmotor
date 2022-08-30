from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_print_qr(self):
        report_name = \
            'gst_lvl_reports.report_label_qr_fabrication_lot_imei_plus_mac'
        return self.env.ref(report_name).report_action(self)

    def button_print_packaging(self):
        report_name = \
            'gst_lvl_reports.report_label_report_packaging'
        return self.env.ref(report_name).report_action(self)


class StockMove(models.Model):
    _inherit = "stock.move"

    # def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
    #     """Auto-assign as done the quantity proposed for the lots"""
    #     self.ensure_one()
    #     res = super()._prepare_move_line_vals(quantity, reserved_quant)
    #     res.update({"qty_done": res.get("product_uom_qty", 0.0)})
    #     return res


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    app_type = fields.Selection(
        related="lot_id.device_id.app_type",
        store=True,
        string="App type",
    )

    subscription_time = fields.Integer(
        related="lot_id.device_id.subscription_time",
        store=True,
        string="Subscription time",
    )


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    def action_open_picking(self):
        """Smart button action to show all pickings for the current lot."""
        self.ensure_one()
        return {
            'name': 'Albaranes',
            'view_type': 'tree',
            'view_mode': 'list',
            'res_model': 'stock.picking',
            'type': 'ir.actions.act_window',
            'context': self._context,
            'domain': [('product_lot', '=', self.id),
                       ('sale_id', '!=', False)],
            'view_id': self.env.ref('stock.vpicktree').id,
            'help': f"""<p class="o_view_nocontent_empty_folder">No pickings 
                        for {self.name}</p>
                        <p>This view shows all pickings for the given lot.</p>
                        """
        }

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Auto set next secuence value for the given product to lot's name."""
        self.ensure_one()
        sequence = self.product_id and self.product_id.sequence_id
        if sequence:
            self.name = sequence.next_by_id()
