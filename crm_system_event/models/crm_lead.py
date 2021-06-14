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
                'system_event_id':
                self.env['system.event'].create({
                    'event_model_id': record.id
                }).id
            })

        return result

    def write(self, vals):
        CRMEventData = self.env['crm.event.data']
        SystemEvent = self.env['system.event']

        old_stage = self.stage_id
        old_user = self.user_id
        result = super(Lead, self).write(vals)

        # Create system event
        if old_user or old_stage:
            CRMEventData.create({
                'system_event_id': SystemEvent.create({
                    'event_model_id': self.id
                }).id,
                'old_stage_id': old_stage.id if 'stage_id' in vals else None,
                'new_stage_id': vals.get('stage_id'),
                'old_user_id': old_user.id if 'user_id' in vals else None,
                'new_user_id': vals.get('user_id')
            })

        return result
