# -*- coding: utf-8 -*-
from lxml import etree

from odoo import models, fields, api, _


class Company(models.Model):
    _inherit = 'res.company'

    country_enforce_cities = fields.Boolean(related='country_id.enforce_cities', readonly=True)
    city_id = fields.Many2one('res.city', string='City of Address')

    @api.onchange('city_id')
    def _onchange_city_id(self):
        self.city = self.city_id.name
        self.zip = self.city_id.zipcode
        self.state_id = self.city_id.state_id

    @api.model
    def _fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(Company, self)._fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                    submenu=submenu)
        if view_type == 'form':
            res['arch'] = self._fields_view_get_address(res['arch'])
        return res

    @api.model
    def _fields_view_get_address(self, arch):
        # render the partner address accordingly to address_view_id
        doc = etree.fromstring(arch)
        if doc.xpath("//field[@name='city_id']"):
            return arch

        replacement_xml = """
                <div>
                    <field name="country_enforce_cities" invisible="1"/>
                    <field name="country_id" invisible="1"/>
                    <field name='city' placeholder="%(placeholder)s"
                        attrs="{
                            'invisible': [('country_enforce_cities', '=', True), ('city_id', '!=', False)],
                        }"
                    />
                    <field name='city_id' placeholder="%(placeholder)s" string="%(placeholder)s"
                        context="{'default_country_id': country_id}"
                        domain="[('country_id', '=', country_id)]"
                        attrs="{
                            'invisible': [('country_enforce_cities', '=', False)],
                        }"
                    />
                </div>
            """

        replacement_data = {
            'placeholder': _('City'),
        }

        def _arch_location(node):
            in_subview = False
            view_type = False
            parent = node.getparent()
            while parent is not None and (not view_type or not in_subview):
                if parent.tag == 'field':
                    in_subview = True
                elif parent.tag in ['list', 'tree', 'kanban', 'form']:
                    view_type = parent.tag
                parent = parent.getparent()
            return {
                'view_type': view_type,
                'in_subview': in_subview,
            }

        for city_node in doc.xpath("//field[@name='city']"):
            location = _arch_location(city_node)
            replacement_data['parent_condition'] = ''
            if location['view_type'] == 'form' or not location['in_subview']:
                replacement_data['parent_condition'] = ", ('parent_id', '!=', False)"

            replacement_formatted = replacement_xml % replacement_data
            for replace_node in etree.fromstring(replacement_formatted).getchildren():
                city_node.addprevious(replace_node)
            parent = city_node.getparent()
            parent.remove(city_node)

        arch = etree.tostring(doc, encoding='unicode')
        return arch
