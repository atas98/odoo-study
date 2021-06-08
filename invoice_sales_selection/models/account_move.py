# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InvoiceSalesSelection(models.Model):

    _inherit = 'account.move.line'

    sales_quality = fields.Selection(selection=[('std', 'Standart'),
                                                ('silver', 'Silver'),
                                                ('gold', 'Gold')],
                                     default="std")
