# -*- coding: utf-8 -*-

from itertools import product
from odoo import models, fields
from datetime import datetime as dt
from datetime import time as t


class PurchaseAutoserialForLots(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        StockMove = self.env['stock.move.line']
        StockLot = self.env['stock.production.lot']

        for picking in self:
            for line in picking.move_line_ids:
                lot_id_exists = picking.move_line_ids.search_count([
                    '&', ('product_id', '=', line.product_id.id), '|',
                    ('lot_id', '!=', False), ('lot_name', '!=', False)
                ])
                if not line.product_id.tracking == 'lot' or lot_id_exists:
                    continue

                # Change lot_name to new serial
                # with format [yy][mm][dd]/[3 digit index of todays lines]
                lines_today_count = StockMove.search_count([
                    ('date', '>=', dt.combine(dt.now(), t.min)),
                    ('date', '<=', dt.combine(dt.now(), t.max))
                ])
                new_serial = dt.today().strftime(r'%y%m%d') + \
                                '/' + str(lines_today_count).zfill(3)

                line.lot_id = StockLot.create({
                    'name': new_serial,
                    'product_id': line.product_id.id,
                    'company_id': line.company_id.id
                }).id

        return super(PurchaseAutoserialForLots, self).button_validate()
