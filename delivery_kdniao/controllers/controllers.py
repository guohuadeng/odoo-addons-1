# -*- coding: utf-8 -*-
from odoo import http


class DeliveryKdniao(http.Controller):
    @http.route('/delivery_kdniao/traceback/<shipper_code>/<carrier_tracking_ref>', auth='public')
    def index(self, shipper_code, carrier_tracking_ref, **kw):
        return http.request.render("delivery_kdniao.traceback_view",
                                   {'shipper_code': shipper_code, 'carrier_tracking_ref': carrier_tracking_ref})
