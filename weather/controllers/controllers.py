# -*- coding: utf-8 -*-
# from odoo import http


# class Weather(http.Controller):
#     @http.route('/weather/weather/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/weather/weather/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('weather.listing', {
#             'root': '/weather/weather',
#             'objects': http.request.env['weather.weather'].search([]),
#         })

#     @http.route('/weather/weather/objects/<model("weather.weather"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('weather.object', {
#             'object': obj
#         })
