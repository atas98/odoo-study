# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CollectiveAccount(models.Model):
    _name = 'collective_account.collective_account'
    _description = 'Managing partner-product relation'

    partner_id = fields.Many2one('res.partner', required=True)
    product_id = fields.Many2one('product.product', required=True)
    total_quantity = fields.Float(default=0)
    total_price = fields.Float(compute='_compute_total_price')
    
    @api.depends('total_quantity')
    def _compute_total_price(self):
        for r in self:
            r.total_price = r.total_quantity * r.product_id.list_price
