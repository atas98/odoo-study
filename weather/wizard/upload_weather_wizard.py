# -*- coding: utf-8 -*-

import csv
import base64
import logging

from io import StringIO
from odoo import api, fields, models
from odoo.exceptions import UserError


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


class UploadWeather(models.TransientModel):
    _name = 'upload.weather.wizard'
    _description = 'Uploads weather data from csv file'

    weather_file_name = fields.Char()
    weather_file = fields.Binary(required=True)
    parsed = fields.Boolean(default=False)
    uploaded = fields.Boolean(default=False)
    weather_line_ids = fields.One2many('upload.weather.wizard.line',
                                       'upload_weather_wizard_id')

    def _check_city_date_uniqueness(self, city, date):
        return bool(self.env["city.weather"].search([
            '&',
            ('city.name', '=', city),
            ('date', '=', date)
        ]))

    def _check_line_data(self, line):
        can_load = True
        error_description = ""

        # Temperature (format)
        try:
            line_temp = float(line['Temperature'])
        except ValueError:
            can_load = False
            error_description = error_description + \
                "Temperature is not float. "
        else:
            # Temperature (boundaries)
            if not (-80 < line_temp < 80):
                can_load = False
                error_description = error_description + \
                    "Temperature is out of bounds. "
        # Humidity (format)
        try:
            line_humidity = float(line['Humidity'])
        except ValueError:
            can_load = False
            error_description = error_description + \
                "Humidity is not float. "
        else:
            # Humidity (boundaries)
            if not (0 < line_humidity < 100):
                can_load = False
                error_description = error_description + \
                    "Humidity is out of bounds. "
        # Date (format)
        try:
            line_date = fields.Date.from_string(line['Date'])
        except ValueError:
            can_load = False
            error_description = error_description + \
                "Wrong date format. "
        else:
            # Date (boundaries)
            if line_date < fields.Date.today():
                can_load = False
                error_description = error_description + \
                    "Date have to be later than current date. "
        # City (uniqueness)
            elif self._check_city_date_uniqueness(line['City'], line_date):
                can_load = False
                error_description = error_description + \
                    "There is already record for this city with this date. "

        return can_load, error_description

    def parse_weather_file(self):
        """Parses the file and create weather wizard lines based on data."""
        self.ensure_one()

        try:
            decoded_file = base64.b64decode(
                self.weather_file).decode('utf-8')
        except UnicodeDecodeError as e:
            logging.warning(e)
            raise UserError("File is not UTF-8.")
        with StringIO(decoded_file) as fp:
            reader = csv.DictReader(fp)
            # Check if all keys exist
            keys = ('City', 'Date', 'Temperature', 'Humidity')
            if not all(key in reader.fieldnames for key in keys):
                raise UserError(f"Keys {keys} expected in csv.")

            WeatherLine = self.env['upload.weather.wizard.line']

            for row in reader:
                # Validate line
                can_load, error_description = self._check_line_data(row)

                # Create weather line
                WeatherLine.create({
                    'city_name': row['City'],
                    'date': row['Date'],
                    'temperature_c': row['Temperature'],
                    'humidity': row['Humidity'],
                    'can_load': can_load,
                    'error_description': error_description,
                    'upload_weather_wizard_id': self.id
                })

        self.parsed = True
        return {
            'view_mode': 'form',
            'res_model': 'upload.weather.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'Parse data',
            'res_id': self.id
        }

    def upload_weather(self):
        """Creates weather records for city.weather model if it does not exist for city and date.
           Creates a city if it does not exist.
           Uploads only data where the field can_load is True."""
        self.ensure_one()

        ukraine = self.env.ref('base.ua')
        ResCity = self.env['res.city']
        WeatherLine = self.env['upload.weather.wizard.line']
        CityWeather = self.env['city.weather']

        for line in self.weather_line_ids:
            if not line.can_load:
                continue
            city = ResCity.search([('name', '=', line.city_name)])
            if not city:
                # If there is no such city create new record
                city = ResCity.create({
                    'name': line.city_name,
                    'country_id': ukraine.id
                })
            date = fields.Date.from_string(line.date)
            temperature_c = float(line.temperature_c)
            humidity = float(line.humidity)
            CityWeather.create({
                'city': city.id,
                'date': date,
                'humidity': humidity,
                'temperature_c': temperature_c
            })
        # Remove processed lines
        self.weather_line_ids.filtered(lambda r: r.can_load == True).unlink()

        self.uploaded = True
        return {
            'view_mode': 'form',
            'res_model': 'upload.weather.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'Parse data',
            'res_id': self.id
        }

    def close_window(self):
        """Ok button handler for closing window"""
        return {
            'type': 'ir.actions.client',
            'tag': 'reload'
        }
