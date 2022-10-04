from odoo import api, fields, models
import base64

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self.send_email_with_attachment()

        return res



    def send_email_with_attachment(self):
       # report_template_id = self.env.ref(
       #     'sale.action_report_saleorder')._render_qweb_pdf(self.id)
       # data_record = base64.b64encode(report_template_id[0])
       # ir_values = {
       #     'name': "Customer Report",
       #     'type': 'binary',
       #     'datas': data_record,
       #     'store_fname': data_record,
       #     'mimetype': 'application/x-pdf',
       # }
       # data_id = self.env['ir.attachment'].create(ir_values)
       emailsend_ids = self.env['ir.mail_server'].search([], order="sequence ASC", limit=1)
       emailsend = "admin@innotek.co.id"
       nameemailsend = ""
       for s in emailsend_ids:
           emailsend = s.smtp_user
           nameemailsend = s.name

       model_data_obj = self.env['ir.model.data']
       qmr = model_data_obj.get_object_reference('sales_team', 'group_sale_manager')[1]

       groups = self.env['res.groups'].search([('id', '=', qmr)])
       for g in groups:
           for u in g.users:
               email_from = "" + nameemailsend + " <" + emailsend + ">"
               template = self.env.ref('mh_sales_email.email_template_notif_sale')
               # template = self.template_id
               # template.attachment_ids = [(6, 0, [data_id.id])]
               email_values = {'email_to': u.login,
                               'email_from': email_from}
               template.send_mail(self.id, email_values=email_values, force_send=True)
       # template.attachment_ids = [(3, data_id.id)]
       return True