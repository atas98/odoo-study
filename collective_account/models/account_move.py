# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        self.ensure_one()

        CollectiveAccount = self.env['collective_account.collective_account']
        for line_id in self.invoice_line_ids:
            collective_account = CollectiveAccount.search(
                [('partner_id', '=', self.partner_id.id),
                 ('product_id', '=', line_id.product_id.id)]
            )
            # Check if collective_account exists
            if collective_account:
                collective_account.total_quantity = collective_account.total_quantity + \
                                              line_id.quantity
            else:
                CollectiveAccount.create({
                    'partner_id': self.partner_id.id,
                    'product_id': line_id.product_id.id,
                    'total_quantity': line_id.quantity
                })

        return super(AccountMove, self).action_post()
