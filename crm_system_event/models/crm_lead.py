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

        # Create event if stage changes
        if 'stage_id' in vals:
            # Create system event
            CRMEventData.create({
                'system_event_id': SystemEvent.create({
                    'event_model_id': self.id
                }).id,
                'old_stage_id': self.stage_id.id,
                'new_stage_id': vals['stage_id']
            })

        # Create event if salesperson changes
        if 'user_id' in vals:
            CRMEventData.create({
                'system_event_id': SystemEvent.create({
                    'event_model_id': self.id
                }).id,
                'old_user_id': self.user_id.id,
                'new_user_id': vals['user_id']
            })

        return super(Lead, self).write(vals)
