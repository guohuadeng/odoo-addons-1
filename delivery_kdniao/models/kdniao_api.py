# -*- coding: utf-8 -*-
import json
import urllib
import base64
import hashlib

from requests import request

from odoo import _
from odoo.exceptions import UserError


class Kdniao(object):
    def __init__(self, prod_environment, debug_logger):
        self.debug_logger = debug_logger
        self.headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "charset": "utf-8"
        }
        self.timeout = 10
        if not prod_environment:
            self.url = "http://testapi.kdniao.com:8081"
        else:
            self.url = "http://api.kdniao.com"
        self.order_service_path = "/api/EOrderService"
        self.order_service_url = self.url + self.order_service_path

    def _check_address(self, partner, check_type='shipper'):
        info = _("Shipper")
        if check_type == 'consignee':
            info = _("Consignee")
        if not partner.name:
            raise UserError(_('%s can not be empty!' % info))
        if not partner.city:
            raise UserError(_('%s city cannot be empty!' % info))
        if not partner.street and not partner.street2:
            raise UserError(_('%s streets and streets 2 cannot be empty!' % info))
        # 公司只有phone字段,没有mobile字段
        if hasattr(partner, 'mobile'):
            if not partner.mobile and not partner.phone:
                raise UserError(_('%s mobile and phone cannot be empty!' % info))
        else:
            if not partner.phone:
                raise UserError(_('%s phone cannot be empty!' % info))

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

    def encrypt(self, app_key, json_data):
        hashlib.md5((json_data + app_key).encode(encoding='UTF-8')).hexdigest()
        md5_str = hashlib.md5((json_data + app_key).encode(encoding='UTF-8')).hexdigest()
        base64_str = bytes.decode(base64.b64encode(md5_str.encode('utf-8')))
        data_sign = urllib.parse.quote(base64_str)
        return data_sign

    def api_request(self, url, app_key, business_id, data, request_type, method="POST"):
        json_data = json.dumps(data)
        request_data = {
            'RequestData': urllib.parse.quote(json_data),
            'EBusinessID': business_id,
            'RequestType': request_type,
            'DataSign': self.encrypt(app_key, json_data),
            'DataType': 2
        }
        try:
            self.debug_logger("%s\n%s" % (url, json_data), 'kdniao_request')
            result = request(
                method=method,
                url=url,
                data=request_data,
                timeout=self.timeout,
                headers=self.headers
            )
            self.debug_logger("%s\n%s" % (result.status_code, result.text), 'kdniao_request')
            if result.status_code != 200:
                raise UserError(_('Request interface failed，status_code %s' % result.status_code))
            kdniao_res = json.loads(result.text)
            if kdniao_res['Success']:
                return kdniao_res
            else:
                raise UserError(_('Failed to create electronic face sheet，error：%s' % kdniao_res['Reason']))
        except Exception as e:
            raise e

    def order_create(self, picking, carrier):
        dict_response = {'tracking_number': 0.0,
                         'price': 0.0,
                         'currency': False}
        # 客户地址-收件人
        self._check_address(picking.partner_id)
        # 公司地址-发件人
        self._check_address(picking.partner_id, 'consignee')
        request_data = {
            'ShipperCode': carrier.kdnniao_shipper_code,
            'OrderCode': picking.name,
            'PayType': 1,
            'ExpType': 1,
            'Sender': self.kdniao_format_address(picking.company_id),
            'Receiver': self.kdniao_format_address(picking.partner_id),
            "Commodity": [{'GoodsName': "其他"}]
        }

        if carrier.kdnniao_customer_name:
            request_data['CustomerName'] = carrier.kdnniao_customer_name
        if carrier.kdnniao_customer_pwd:
            request_data['CustomerPwd'] = carrier.kdnniao_customer_pwd
        result = self.api_request(self.order_service_url,
                                  carrier.kdnniao_api_key,
                                  carrier.kdnniao_business_id,
                                  request_data,
                                  1007)
        dict_response['tracking_number'] = result['Order']['LogisticCode']
        return dict_response

    def order_cancel(self, picking, carrier):
        request_data = {
            'ShipperCode': carrier.kdnniao_shipper_code,
            'OrderCode': picking.name,
            'ExpNo': picking.carrier_tracking_ref,
        }
        if carrier.kdnniao_customer_name:
            request_data['CustomerName'] = carrier.kdnniao_customer_name
        if carrier.kdnniao_customer_pwd:
            request_data['CustomerPwd'] = carrier.kdnniao_customer_pwd
        result = self.api_request(self.order_service_url,
                                  carrier.kdnniao_api_key,
                                  carrier.kdnniao_business_id,
                                  request_data,
                                  1147)
