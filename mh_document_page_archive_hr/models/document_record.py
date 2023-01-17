from odoo import fields, models, api

from datetime import date,datetime
from dateutil.relativedelta import relativedelta
import time

class record_document(models.Model):
    _inherit = 'record.document'

    employee_id = fields.Many2one('hr.employee', 'Employee', readonly=True, states={'draft':[('readonly', False)]})

