# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SystemEvent(models.Model):
    _name = 'system.event'
    _rec_name = 'event_model_id'

    event_model_id = fields.Many2one('crm.lead', readonly=True, ondelete='cascade')
