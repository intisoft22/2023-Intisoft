from odoo import fields, models, api

class DocumentPage(models.Model):
    """This class is use to manage Document."""

    _inherit = "document.page"

    dept_id = fields.Many2one( "hr.department", "Department", )
