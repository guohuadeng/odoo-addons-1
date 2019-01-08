# -*- coding: utf-8 -*-
from odoo import http

# class DeliveryKdniao(http.Controller):
#     @http.route('/delivery_kdniao/delivery_kdniao/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/delivery_kdniao/delivery_kdniao/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('delivery_kdniao.listing', {
#             'root': '/delivery_kdniao/delivery_kdniao',
#             'objects': http.request.env['delivery_kdniao.delivery_kdniao'].search([]),
#         })

#     @http.route('/delivery_kdniao/delivery_kdniao/objects/<model("delivery_kdniao.delivery_kdniao"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('delivery_kdniao.object', {
#             'object': obj
#         })