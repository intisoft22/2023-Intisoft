from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    attachment_ids = fields.Many2many('ir.attachment', 'sale_order_ir_attachments_rel',
                                      'sale_id', 'attachment_id', string="Attachments", states={'done': [('readonly', True)]}
                                      )