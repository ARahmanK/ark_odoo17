# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class ProductInfoReportWizard(models.TransientModel):
    _name = 'product.info.report.wizard'
    _description = 'Product Information Wizard'

    is_all_products = fields.Boolean('All Products', default=False)
    category_id = fields.Many2one('product.category', string='Product Category')
    product_ids = fields.Many2many('product.product', string='Product')

    def action_print_report(self):
        """
            This function is responsible for generating a report based on the selected product or category.
            It checks if either a product or a category is selected. If neither is selected, it raises a ValidationError.
            If a product is selected, it retrieves the product data using the product.product model and stores it in the 'products' variable.
            If a category is selected, it retrieves the product ids using the product.product model and checks if any products exist for the category.
            If products exist, it stores the product ids in the 'products' variable and creates a dictionary with the 'products' key and the product ids as the value.
            If no products exist for the category, it raises a ValidationError.
            Finally, it returns the report action for the 'product_info_report.action_report_product_detailed_pdf' report with the 'self' record and the 'data' dictionary as parameters.
        """
        if self.is_all_products:
            data = {
                'products': self.env['product.product'].search_read([]),
            }
        elif not self.product_ids and not self.category_id:
            raise ValidationError('Kindly select Category or a Product!')

        elif self.product_ids:
            data = {
                'products': self.env['product.product'].search_read([('id', 'in', self.product_ids.ids)]),
            }
        elif self.category_id:
            product_ids = self.env['product.product'].search_read([('categ_id', '=', self.category_id.id)])
            if product_ids:
                data = {
                    'products': product_ids,
                }
            else:
                raise ValidationError('No Product for this Category!')
        return self.env.ref('product_info_report.action_report_product_detailed_pdf').report_action(self, data=data)

    def button_cancel(self):
        return True
