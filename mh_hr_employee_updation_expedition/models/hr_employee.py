
from datetime import datetime, timedelta
from odoo import models, fields, _, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    nik_kna = fields.Char("NIK KNA")
    code_mitra = fields.Char("Partner Code",default="KRIAN081")

    vendor_id = fields.Many2one('res.partner', 'Vendor')
    dp_id = fields.Many2many('dp.location', 'hr_employee_dp_rel', 'employee_id', 'dp_id', 'DP')
    # dp_id = fields.Many2one('dp.location', 'DP')
    joining_kna_date = fields.Date(string='KNA Joining Date',)
    divisi = fields.Char("Division",default="Region")
    status = fields.Char("Employee Status",default="Mitra Aktif")
    letter_sign = fields.Boolean("Statement Letter signature")



class ErmLocation(models.Model):
    _name = 'erm.location'

    name = fields.Char("Name")


class RmLocation(models.Model):
    _name = 'rm.location'

    name = fields.Char("Name")
    erm_id = fields.Many2one('erm.location', 'ERM')

class DpLocation(models.Model):
    _name = 'dp.location'

    name = fields.Char("Name")
    code = fields.Char("Code")
    rm_id = fields.Many2one('rm.location', 'RM')
