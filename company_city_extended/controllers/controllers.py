# -*- coding: utf-8 -*-
from odoo import http

# class CompanyCityExtended(http.Controller):
#     @http.route('/company_city_extended/company_city_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/company_city_extended/company_city_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('company_city_extended.listing', {
#             'root': '/company_city_extended/company_city_extended',
#             'objects': http.request.env['company_city_extended.company_city_extended'].search([]),
#         })

#     @http.route('/company_city_extended/company_city_extended/objects/<model("company_city_extended.company_city_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('company_city_extended.object', {
#             'object': obj
#         })