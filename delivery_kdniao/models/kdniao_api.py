# -*- coding: utf-8 -*-
import json
import urllib
import base64
import hashlib

from requests import request


class Kdniao(object):
    def __init__(self, EBusinessID, AppKey, **kwargs):
        self.EBusinessID = EBusinessID
        self.AppKey = AppKey
        self.timeout = 10
        self.environment = kwargs.get('environment', False)
        self.url = "http://api.kdniao.com"
        self.headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "charset": "utf-8"
        }
        self.order_service_path = "/api/EOrderService"

        if not self.environment:
            self.url = "http://testapi.kdniao.com:8081"

        self.order_service_url = self.url + self.order_service_path

    def encrypt(self, json_data):
        hashlib.md5((json_data + self.AppKey).encode(encoding='UTF-8')).hexdigest()
        md5_str = hashlib.md5((json_data + self.AppKey).encode(encoding='UTF-8')).hexdigest()
        base64_str = bytes.decode(base64.b64encode(md5_str.encode('utf-8')))
        data_sign = urllib.parse.quote(base64_str)
        return data_sign

    def order_create(self, json_data):
        data = {
            'RequestData': urllib.parse.quote(json_data),
            'EBusinessID': self.EBusinessID,
            'RequestType': 1007,
            'DataSign': self.encrypt(json_data),
            'DataType': 2
        }
        result = request(
            method="POST",
            url=self.order_service_url,
            data=data,
            timeout=self.timeout,
            headers=self.headers
        )
        return result

    def order_cancel(self, json_data):
        data = {
            'RequestData': urllib.parse.quote(json_data),
            'EBusinessID': self.EBusinessID,
            'RequestType': 1147,
            'DataSign': self.encrypt(json_data),
            'DataType': 2
        }
        result = request(
            method="POST",
            url=self.order_service_url,
            data=data,
            timeout=self.timeout,
            headers=self.headers
        )
        return result
