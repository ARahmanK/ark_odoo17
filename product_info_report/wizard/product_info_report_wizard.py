# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class ProductInfoReportWizard(models.TransientModel):
    _name = 'product.info.report.wizard'

    # def default_product_ids(self):
    #     products = self.env['product.template'].sudo().search([('categ_id', '=', self.product_categ_id.id)])
    #     if products:
    #         return [('id', 'in', products.ids)]
    #     else:
    #         return [(0, '=', 1)]

    product_categ_id = fields.Many2one(
        'product.category',
        string='Product Category'
    )
    product_id = fields.Many2one('product.product', string='Product')

    # @api.onchange('product_categ_id', 'product_tmpl_id')
    # def onchange_product_categ_id(self):
    #     products = self.env['product.template'].sudo().search([('categ_id', '=', self.product_categ_id.id)])
    #     if products:
    #         return {'domain': {'product_tmpl_id': [('categ_id', '=', self.product_categ_id.id)]}}
    #     else:
    #         return {'domain': {'product_tmpl_id': []}}

    def action_print_report(self):
        if not self.product_id and not self.product_categ_id:
            raise ValidationError('Kindly select Category or a Product!')
        if self.product_id:
            products = self.product_id
            data = {
                'products': self.env['product.product'].search_read([('id', '=', self.product_id.id)]),
            }
        elif self.product_categ_id:
            product_ids = self.env['product.product'].search_read([('categ_id', '=', self.product_categ_id.id)])
            if product_ids:
                products = product_ids
                data = {
                    'products': products,
                }
            else:
                raise ValidationError('No Product for this Category!')
        return self.env.ref('product_info_report.action_report_product_detailed_pdf').report_action(self, data=data)

    def button_cancel(self):
        return True
