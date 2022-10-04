from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    attachment_ids = fields.Many2many('ir.attachment', 'account_move_ir_attachments_rel',
                                      'account_move_id', 'attachment_id', string="Attachments", states={'done': [(
            'readonly', True)]}
                                      )