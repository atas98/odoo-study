# -*- coding: utf-8 -*-

from itertools import product
from odoo import models, fields
from datetime import datetime as dt
from datetime import time as t


class PurchaseAutoserialForLots(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        StockMove = self.env['stock.move.line']
        for picking in self:
            for line in picking.move_line_ids:
                if line.product_id.tracking == 'lot':
                    # Change lot_name to new serial
                    # with format [yy][mm][dd]/[3 digit index of todays lines]
                    lines_today_count = StockMove.search_count([
                        ('date', '>=', dt.combine(dt.now(), t.min)),
                        ('date', '<=', dt.combine(dt.now(), t.max)),
                    ])
                    if not line.lot_id:
                        new_serial = dt.today().strftime(r'%y%m%d') + \
                                     '/' + str(lines_today_count).zfill(3)
                        line.lot_id = self.env['stock.production.lot'].create({
                            'name': new_serial,
                            'product_id': line.product_id.id,
                            'company_id': line.company_id.id
                        }).id

        return super(PurchaseAutoserialForLots, self).button_validate()
