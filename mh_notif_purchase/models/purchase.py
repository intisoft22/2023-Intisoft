from odoo import api, fields, models, _

from datetime import datetime

class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = 'purchase.order'

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
        'to approve': [('readonly', True)],
    }

    check_user = fields.Boolean(
        string="Check User", store=True,
        compute="_get_checkuser"
    )
    check_user2 = fields.Boolean(
        string="Check User",
        compute="_get_checkuser"
    )
    order_line = fields.One2many('purchase.order.line', 'order_id', string='Order Lines'
                                 , states={'to approve': [('readonly', True)],'purchase': [('readonly', True)],'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True, states=READONLY_STATES,
                                 change_default=True, tracking=True,
                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                 help="You can find a vendor by its Name, TIN, Email or Internal Reference.")
    date_order = fields.Datetime('Order Deadline', required=True, states=READONLY_STATES, index=True, copy=False,
                                 default=fields.Datetime.now,
                                 help="Depicts the date within which the Quotation should be confirmed and converted into a purchase order.")

    @api.depends('user_id')
    def _get_checkuser(self):
        for x in self:

            x.check_user2 = False
            if x.state == 'draft':
                if self.env.user.id == x.user_id.id:
                    x.check_user2 = True



    def button_approve(self, force=False):
        res = super(PurchaseOrder, self).button_approve()
        activity = self.env['mail.activity'].sudo().create({
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            'note': _(
                'this document approved.'),
            'res_id': self.id,
            'user_id': self.user_id.id,
            'date_deadline': datetime.today(),
            'res_model_id': self.env.ref('purchase.model_purchase_order').id,
        })
        activity.write({'user_id': self.user_id.id,})
        # activity._onchange_activity_type_id()

        return res



    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()

        model_data_obj = self.env['ir.model.data']
        qmr = model_data_obj.get_object_reference('purchase', 'group_purchase_manager')[1]

        groups = self.env['res.groups'].search([('id', '=', qmr)])
        for g in groups:
            for u in g.users:
                # print(u.name)
                vals={
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'note': _(
                        'this document need approval.'),
                    'res_id': self.id,
                    'user_id': u.id,
                    'date_deadline': datetime.today(),
                    'res_model_id': self.env.ref('purchase.model_purchase_order').id,
                }
                # print(vals)
                activity = self.env['mail.activity'].sudo().create(vals)
                activity.sudo().write({'user_id': u.id,})
                # activity._onchange_activity_type_id()
        return res