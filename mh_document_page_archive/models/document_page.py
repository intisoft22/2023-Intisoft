from odoo import fields, models, api

class DocumentPage(models.Model):
    """This class is use to manage Document."""

    _inherit = "document.page"

    record_ids = fields.One2many('record.document', 'jenis', 'Record List', readonly=True)
