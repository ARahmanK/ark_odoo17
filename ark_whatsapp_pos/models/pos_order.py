# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,UserError



class PosOrder(models.Model):
    _inherit = 'pos.order'

    def action_sent_receipt_on_whatsapp(self, name, partner, ticket_image):
        """ Send receipt on whatsapp if whatsapp is enabled and partner has whatsapp number or number is provided."""
        self.ensure_one()

        # Validate required conditions
        if not self.config_id.whatsapp_enabled:
            raise UserError(_("WhatsApp integration is not enabled for this POS."))
        if not self.config_id.receipt_template_id:
            raise UserError(_("No WhatsApp receipt template configured for this POS."))
        if not partner.get('whatsapp'):
            raise UserError(_("Customer has no WhatsApp number configured."))

        # Create receipt attachment
        filename = f'Receipt-{name}.pdf'  # Changed to PDF for better compatibility
        receipt_attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'datas': ticket_image,
            'res_model': 'pos.order',
            'res_id': self.id,
            'mimetype': 'application/pdf',  # Changed to PDF mime type
        })

        try:
            # Generate invoice PDF if available
            invoice_attachment = False
            if self.account_move:
                invoice_report = self.env.ref('account.account_invoices')
                invoice_pdf, _ = invoice_report._render_qweb_pdf(self.account_move.ids)
                invoice_filename = f'Invoice-{self.account_move.name}.pdf'
                invoice_attachment = self.env['ir.attachment'].create({
                    'name': invoice_filename,
                    'type': 'binary',
                    'datas': base64.b64encode(invoice_pdf),
                    'res_model': 'pos.order',
                    'res_id': self.id,
                    'mimetype': 'application/pdf',
                })

            # Prepare attachments list
            attachments = [(4, receipt_attachment.id)]
            if invoice_attachment:
                attachments.append((4, invoice_attachment.id))

            # Create and send WhatsApp message
            whatsapp_composer = self.env['acrux.chat.message.wizard'].sudo().create({
                'partner_id': self.partner_id.id,
                'number': partner['whatsapp'],
                'new_number': True,
                'template_id': self.config_id.receipt_template_id.id,
                'connector_id': 1,  # Make this configurable if you have multiple connectors
                'model': 'pos.order',
                'res_id': self.id,
                'attachment_ids': attachments,
                'text': ('Here is your receipt from %s') % self.company_id.name
            })

            whatsapp_composer.send_message_wizard()
            return {
                'success': True,
                'message': 'Receipt successfully sent via WhatsApp'
            }

        except Exception as e:
            # Clean up attachments if something fails
            receipt_attachment.unlink()
            if invoice_attachment:
                invoice_attachment.unlink()
            raise UserError("Failed to send WhatsApp message: %s") % str(e)

    # def action_sent_receipt_on_whatsapp(self, name, partner, ticket_image):
    #     """ Send receipt on whatsapp if whatsapp is enabled and partner has whatsapp number or number is provided."""
    #     if not self or not self.config_id.whatsapp_enabled or not self.config_id.receipt_template_id or not partner.get('whatsapp'):
    #         return
    #     self.ensure_one()
    #     filename = 'Receipt-' + name + '.jpg'
    #     receipt = self.env['ir.attachment'].create({
    #         'name': filename,
    #         'type': 'binary',
    #         'datas': ticket_image,
    #         'res_model': 'pos.order',
    #         'res_id': self.ids[0],
    #         'mimetype': 'image/jpeg',
    #     })
    #
    #     whatsapp_composer = self.env['acrux.chat.message.wizard'].sudo().create(
    #         {
    #             'partner_id': self.partner_id.id,
    #             'attachment_ids': [(4,receipt.id)],
    #             'number': partner['whatsapp'],
    #             'template_id': self.config_id.receipt_template_id.id,
    #             'connector_id':1,
    #             'model': 'pos.order',
    #             'res_id': self.id,
    #             'text': 'Here is your attachment and data is fetched from python'
    #         }
    #     )
    #     whatsapp_composer.send_message_wizard()



        # whatsapp_composer = self.env['whatsapp.composer'].with_context({'active_id': self.id}).create(
        #     {
        #         'attachment_id': receipt.id,
        #         'phone': partner['whatsapp'],
        #         'wa_template_id': self.config_id.receipt_template_id.id,
        #         'res_model': 'pos.order'
        #     }
        # )
        # whatsapp_composer._send_whatsapp_template()
        # if self.to_invoice and self.config_id.invoice_template_id:
        #     whatsapp_composer = self.env['whatsapp.composer'].with_context({'active_id': self.account_move.id}).create(
        #         {
        #             'phone': partner['whatsapp'],
        #             'wa_template_id': self.config_id.invoice_template_id.id,
        #             'res_model': 'account.move'
        #         }
        #     )
        #     # Receipt is already send so force_send_by_cron is True
        #     # so it's not raise error if there is any miss configuration
        #     whatsapp_composer._send_whatsapp_template(force_send_by_cron=True)

    def _get_whatsapp_safe_fields(self):
        return {'partner_id.name', 'name', 'company_id.name'}

    def _mail_get_partners(self):
        return {pos_order.id: pos_order.partner_id for pos_order in self}
