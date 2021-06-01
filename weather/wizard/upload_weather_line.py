# -*- coding: utf-8 -*-

from odoo import api, fields, models


class UploadWeatherLine(models.TransientModel):
    _name = 'upload.weather.wizard.line'
    _description = 'Represents a line of data for UploadWeather wizard'

    upload_weather_wizard_id = fields.Many2one('upload.weather.wizard',
                                               'weather_line_ids',
                                               readonly=True)
    city_name = fields.Char(readonly=True)
    temperature_c = fields.Char(readonly=True)
    humidity = fields.Char(readonly=True)
    date = fields.Char(readonly=True)
    error_description = fields.Char(readonly=True)
    can_load = fields.Boolean(default=True)
