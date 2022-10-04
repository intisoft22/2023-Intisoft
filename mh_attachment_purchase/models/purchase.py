from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    attachment_ids = fields.Many2many('ir.attachment', 'purchase_order_ir_attachments_rel',
                                      'purchase_id', 'attachment_id', string="Attachments", states={'done': [(
            'readonly', True)]}
                                      )