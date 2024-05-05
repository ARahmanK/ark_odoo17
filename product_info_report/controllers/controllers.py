# -*- coding: utf-8 -*-
# from odoo import http


# class ProductInfoReport(http.Controller):
#     @http.route('/product_info_report/product_info_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_info_report/product_info_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_info_report.listing', {
#             'root': '/product_info_report/product_info_report',
#             'objects': http.request.env['product_info_report.product_info_report'].search([]),
#         })

#     @http.route('/product_info_report/product_info_report/objects/<model("product_info_report.product_info_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_info_report.object', {
#             'object': obj
#         })

