# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError


class Weather(models.Model):
    _name = "city.weather"
    _description = "Weather forecast for city"

    _sql_constraints = [
        ('unique_date_city', 'UNIQUE (city, date)',
         'There can be only one weather obj for each city'),
        ('temperature_restrictions',
         'CHECK (temperature_c>=-80 AND temperature_c<=80)', 'Wrong temperature'),
        ('temperature_restrictions',
         'CHECK (humidity>=0 AND humidity<=100)', 'Wrong humidity')
    ]

    @api.model
    def _get_default_uom_temperature_c(self):
        return self.env.ref('weather.uom_celsius').id

    @api.model
    def _get_default_uom_temperature_f(self):
        return self.env.ref('weather.uom_fahrenheit').id

    city = fields.Many2one("res.city",
                           required=True,
                           index=True,
                           states={"confirmed": [("readonly", True)]})
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed')],
        default="draft")
    date = fields.Date(required=True,
                       index=True,
                       states={"confirmed": [("readonly", True)]})
    humidity = fields.Float(digits=dp.get_precision('Humidity'),
                            states={"confirmed": [("readonly", True)]})
    temperature_c = fields.Float(string='Celsius',
                                 help='Temperature in degrees centigrade',
                                 digits=dp.get_precision('Temperature'),
                                 states={"confirmed": [("readonly", True)]})
    uom_temperature_c = fields.Many2one('uom.uom',
                                        readonly=True,
                                        required=True,
                                        default=_get_default_uom_temperature_c)
    temperature_f = fields.Float(readonly=True,
                                 compute='_compute_fahrenheit_temperature',
                                 string='Fahrenheit',
                                 help='temperature in degrees fahrenheit',
                                 digits=dp.get_precision('Temperature'))
    uom_temperature_f = fields.Many2one('uom.uom',
                                        readonly=True,
                                        required=True,
                                        default=_get_default_uom_temperature_f)

    @api.depends('temperature_c')
    def _compute_fahrenheit_temperature(self):
        for r in self:
            r.temperature_f = (r.temperature_c * 9/5) + 32

    @api.constrains('date')
    def _compute_temperature_f(self):
        for r in self:
            if r.date < fields.Date.today():
                raise ValidationError('Dates can only start from today')
