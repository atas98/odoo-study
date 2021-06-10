# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CRMEventData(models.Model):
    _name = 'crm.event.data'
    _rec_name = 'record_name'

    record_name = fields.Char(compute='_compute_record_name')
    system_event_id = fields.Many2one('system.event',
                                      readonly=True,
                                      ondelete='cascade',
                                      delegate=True)
    old_user_id = fields.Many2one('res.users',
                                  readonly=True,
                                  ondelete='cascade')
    new_user_id = fields.Many2one('res.users',
                                  readonly=True,
                                  ondelete='cascade')
    old_stage_id = fields.Many2one('crm.stage',
                                   readonly=True,
                                   ondelete='set null')
    new_stage_id = fields.Many2one('crm.stage',
                                   readonly=True,
                                   ondelete='set null')

    def _compute_record_name(self):
        for r in self:
            r.record_name = ' '.join(
                (r.create_uid.name,
                 r.create_date.strftime(r'%Y-%m-%d %H:%M:%S')))
