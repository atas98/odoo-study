# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseAutoserialForLots(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        StockMove = self.env['stock.move.line']
        for picking in self:
            for line in picking.move_line_ids:
                if line.product_id.tracking == 'lot':
                    # Change lot_name to new serial
                    # with format [yy][mm][dd]/[3 digit index of todays lines]
                    lines_today_count = StockMove.search([
                        ('date', '>=',
                         fields.Datetime.now().strftime('%Y-%m-%d 00:00:00')
                         ),
                        ('date', '<=',
                         fields.Datetime.now().strftime('%Y-%m-%d 23:23:59'))
                    ])
                    line.lot_name = fields.Datetime.today().strftime(r'%y%m%d') + \
                                    '/' + str(lines_today_count).zfill(3)
                    line.qty_done = line.product_uom_qty

        return super(PurchaseAutoserialForLots, self).button_validate()
