# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Weather(models.Model):
    _name = "city.weather"
    _description = "Weather forecast for city"

    @api.model
    def _get_default_uom_temperature_c(self):
        return self.env.ref('weather.uom_celsius')

    @api.model
    def _get_default_uom_temperature_f(self):
        return self.env.ref('weather.uom_fahrenheit')

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
    humidity = fields.Float(digits='Humidity',
                            states={"confirmed": [("readonly", True)]})
    temperature_c = fields.Float(string='Celsius',
                                 help='Temperature in degrees centigrade',
                                 digits='Temperature',
                                 states={"confirmed": [("readonly", True)]})
    uom_temperature_c = fields.Many2one('uom.uom',
                                        readonly=True,
                                        required=True,
                                        default=_get_default_uom_temperature_c)
    temperature_f = fields.Float(readonly=True,
                                 compute='_compute_fahrenheit_temperature',
                                 store=True,
                                 string='Fahrenheit',
                                 help='temperature in degrees fahrenheit',
                                 digits='Temperature')
    uom_temperature_f = fields.Many2one('uom.uom',
                                        readonly=True,
                                        required=True,
                                        default=_get_default_uom_temperature_f)
    
    _sql_constraints = [
        ('unique_date_city', 'UNIQUE (city, date)',
         'There can be only one weather obj for each city'),
        ('temperature_restrictions',
         'CHECK (temperature_c>=-80 AND temperature_c<=80)', 'Wrong temperature'),
        ('humidity_restrictions',
         'CHECK (humidity>=0 AND humidity<=100)', 'Wrong humidity')
    ]
    
    @api.depends('temperature_c')
    def _compute_fahrenheit_temperature(self):
        for r in self:
            r.temperature_f = (r.temperature_c * 9/5) + 32

    @api.constrains('date')
    def _validate_date_later_then_today(self):
        for r in self:
            if r.date < fields.Date.today():
                raise ValidationError('Dates can only start from today')
