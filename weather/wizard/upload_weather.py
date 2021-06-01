# -*- coding: utf-8 -*-

import re
import csv
import base64

from io import StringIO
from odoo import api, fields, models
from odoo.exceptions import UserError


class UploadWeather(models.TransientModel):
    _name = 'upload.weather.wizard'
    _description = 'Uploads weather data from csv file'

    weather_file_name = fields.Char()
    weather_file = fields.Binary(required=True)
    parsed = fields.Boolean(default=False)
    uploaded = fields.Boolean(default=False)
    weather_line_ids = fields.One2many('upload.weather.wizard.line',
                                       'upload_weather_wizard_id')

    def _check_data(self, line):
        can_load = True
        error_description = ""

        float_pattern = re.compile(r"\d+.{0,1}\d+")
        date_pattern = re.compile(r"\d+.{0,1}\d+")

        # Temperature (format)
        if not re.match(float_pattern, line['Temperature']):
            can_load = False
            error_description = error_description + "Temperature is not float. "
        # Temperature (boundaries)
        elif not (-80 < float(line['Temperature']) < 80):
            can_load = False
            error_description = error_description + "Temperature is out of bounds. "
        # Humidity (format)
        if not re.match(float_pattern, line['Humidity']):
            can_load = False
            error_description = error_description + "Humidity is not float. "
        # Humidity (boundaries)
        elif not (0 < float(line['Humidity']) < 100):
            can_load = False
            error_description = error_description + "Humidity is out of bounds. "
        # Date (format)
        if not re.match(date_pattern, line['Date']):
            can_load = False
            error_description = error_description + "Wrong date format. "
        # Date (boundaries)
        elif fields.Date.from_string(line['Date']) < fields.Date.today():
            can_load = False
            error_description = error_description + \
                "Date have to be later than current date. "
        # City (uniqueness)
        elif self.env["city.weather"].search([
            '&',
            ('city.name', '=', line['City']),
            ('date', '=', fields.Date.from_string(line['Date']))
        ]):
            can_load = False
            error_description = error_description + \
                "There is already record for this city with this date. "

        return can_load, error_description

    def parse_weather_file(self):
        """Parses the file and create weather wizard lines based on data."""
        self.ensure_one()
        try:
            with StringIO(base64.b64decode(
                    self.weather_file).decode('utf-8')) as fp:
                try:
                    reader = csv.DictReader(fp)
                except csv.Error as e:
                    raise UserError(e)
                created_lines = []
                for row in reader:
                    # Validate line
                    can_load, error_description = self._check_data(row)

                    # Create weather line
                    created_lines.append((0, 0, {
                        'city_name': row['City'],
                        'date': row['Date'],
                        'temperature_c': row['Temperature'],
                        'humidity': row['Humidity'],
                        'can_load': can_load,
                        'error_description': error_description
                    }))
                # Remove processed lines from wizard
                self.weather_line_ids = created_lines
        except Exception as e:
            raise UserError(e)

        self.parsed = True
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'upload.weather.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'Parse data',
            'res_id': self.id,
            'context': self.env.context
        }

    def upload_weather(self):
        """Creates weather records for city.weather model if it does not exist for city and date.
           Creates a city if it does not exist.
           Uploads only data where the field can_load is True."""
        self.ensure_one()
        for line in self.weather_line_ids:
            if line.can_load:
                city = self.env['res.city'].search([('name', '=',
                                                     line.city_name)]).id
                if not city:
                    # if there is no such city create new record
                    country_id = self.env['res.country'].search([
                        ('name', '=', 'Ukraine')
                    ]).id
                    city = self.env['res.city'].create({
                        'name': line.city_name,
                        'country_id': country_id
                    }).id
                date = fields.Date.from_string(line.date)
                temperature_c = float(line.temperature_c)
                humidity = float(line.humidity)
                self.env['city.weather'].create({
                    'city': city,
                    'date': date,
                    'humidity': humidity,
                    'temperature_c': temperature_c
                })
                # Remove processed line
                self.write({'weather_line_ids': [(2, line.id)]})

        self.uploaded = True
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'upload.weather.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'Parse data',
            'res_id': self.id,
            'context': self.env.context
        }

    def close_window(self):
        """Ok button handler for closing window"""
        return None
