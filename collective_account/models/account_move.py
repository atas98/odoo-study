# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        CollectiveAccount = self.env['collective_account.collective_account']
        for r in self:
            for line in r.invoice_line_ids:
                collective_account = CollectiveAccount.search(
                    [('partner_id', '=', r.partner_id.id),
                    ('product_id', '=', line.product_id.id)]
                )
                # Check if collective_account exists
                if collective_account:
                    collective_account.total_quantity = (
                        collective_account.total_quantity + line.quantity
                    )
                else:
                    CollectiveAccount.create({
                        'partner_id': r.partner_id.id,
                        'product_id': line.product_id.id,
                        'total_quantity': line.quantity
                    })

        return super(AccountMove, self).action_post()
