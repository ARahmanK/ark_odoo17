# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    whatsapp_enabled = fields.Boolean('WhatsApp Enabled', default=False)
    # connector_id = fields.Many2one('acrux.chat.connector', string='Channel')
    receipt_template_id = fields.Many2one('mail.template', string="Receipt template", domain=[('model', '=', 'pos.order'), ('is_chatroom_template', '=', True)])
    invoice_template_id = fields.Many2one('mail.template', string="Invoice template", domain=[('model', '=', 'account.move'), ('is_chatroom_template', '=', True)])
