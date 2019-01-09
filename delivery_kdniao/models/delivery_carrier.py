# -*- coding: utf-8 -*-
import json
from .kdniao_api import Kdniao
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    delivery_type = fields.Selection(selection_add=[('kdniao', 'KDNiao')])
    kdnniao_business_id = fields.Char(string="Business ID")
    kdnniao_api_key = fields.Char(string="API KEY")
    kdnniao_customer_name = fields.Char(string="Customer Name")
    kdnniao_customer_pwd = fields.Char(string="Customer Pwd")
    kdnniao_shipper_code = fields.Char(string="Shipper Code")
    kdnniao_template_size = fields.Char(string="Template Size")
    kdnniao_error_message = fields.Char(store=False)

    def _check_address(self, partner):
        self.ensure_one()
        if not partner.name:
            self.kdnniao_error_message = "姓名不能为空！"
            return False
        if not partner.city:
            self.kdnniao_error_message = "城市不能为空！"
            return False
        if not partner.street and not partner.street2:
            self.kdnniao_error_message = "街道和街道2不能都为空！"
            return False
        # 公司只有phone字段,没有mobile字段
        if hasattr(partner, 'mobile'):
            if not partner.mobile and not partner.phone:
                self.kdnniao_error_message = "手机和固话不能都为空！"
                return False
        else:
            if not partner.phone:
                self.kdnniao_error_message = "电话不能都为空！"
                return False
        return True

    def kdniao_format_address(self, partner):
        data = {'Name': '', 'ProvinceName': '', 'CityName': '', 'ExpAreaName': '', 'Address': ''}
        data['Name'] = partner.name
        if "市" in partner.state_id.name:
            data['ProvinceName'] = partner.state_id.name.replace("市", '')
            data['CityName'] = partner.state_id.name
            if partner.city.find('县') == 0:
                data['ExpAreaName'] = partner.city.replace('县', '', 1)
            if partner.city.find('市辖区') == 0:
                data['ExpAreaName'] = partner.city.replace('市辖区', '', 1)
        else:
            data['ProvinceName'] = partner.state_id.name
            if partner.city.find("市") > 0:
                data['CityName'] = partner.city[0:partner.city.find('市') + 1]
                data['ExpAreaName'] = partner.city[partner.city.find('市') + 1:len(partner.city)]
        if partner.street:
            data['Address'] += partner.street
        if partner.street2:
            data['Address'] += partner.street2
        if partner.phone:
            data['Tel'] = partner.phone
        if hasattr(partner, 'mobile'):
            data['Mobile'] = partner.mobile
        return data

    def kdniao_rate_shipment(self, order):
        return {
            'success': True,
            'price': 0,
            'error_message': False,
            'warning_message': False
        }

    def kdniao_send_shipping(self, pickings):
        res = []
        kdniao_api = Kdniao(self.prod_environment, self.log_xml)
        for picking in pickings:
            shipping = kdniao_api.order_create(picking, self)
            logmessage = (_("Shipment created into %s <br/> <b>Tracking Number : </b>%s") % (
                self.name, shipping['tracking_number']))
            picking.message_post(body=logmessage)
            shipping_data = {
                'exact_price': shipping['price'],
                'tracking_number': shipping['tracking_number']
            }
            res = res + [shipping_data]
        return res

    def kdniao_get_tracking_link(self, pickings):
        return "/delivery_kdniao/traceback/%s/%s" % (self.kdnniao_shipper_code, pickings.carrier_tracking_ref)

    def kdniao_cancel_shipment(self, picking):
        kdniao_api = Kdniao(self.prod_environment, self.log_xml)
        kdniao_api.order_cancel(picking, self)
        picking.message_post(body=_(u"You can't cancel %s shipping without pickup date." % self.name))
        picking.write({'carrier_tracking_ref': '',
                       'carrier_price': 0.0})
