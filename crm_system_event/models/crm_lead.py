# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Lead(models.Model):
    _inherit = 'crm.lead'

    @api.model_create_multi
    def create(self, vals_list):
        result = super(Lead, self).create(vals_list)

        for record in result:
            # Create system event
            self.env['crm.event.data'].create({
                'system_event_id': self.env['system.event'].create({
                    'event_model_id': record.id
                }).id
            })

        return result

