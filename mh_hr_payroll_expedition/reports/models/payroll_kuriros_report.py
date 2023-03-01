# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _

from datetime import datetime, timedelta, date
from pytz import timezone
import time


class PayrollKurirOSReportWizard(models.TransientModel):
    _name = 'payroll.kuriros.report.wizard'

    bulan = fields.Selection(
        [('1', 'Januari'), ('2', 'Februari'), ('3', 'Maret'), ('4', 'April'), ('5', 'Mei'), ('6', 'Juni'), ('7', 'Juli'),
         ('8', 'Agustus'), ('9', 'September'), ('10', 'Oktober'), ('11', 'November'), ('12', 'Desember')], 'Bulan',
        default=lambda *a: str(time.gmtime()[1]))
    tahun = fields.Char('Year', default=lambda *a: time.gmtime()[0])

    def get_excel_report(self):
        # redirect ke controller /sale/excel_report untuk generate file excel
        return {
            'type': 'ir.actions.act_url',
            'url': '/payroll/kurir_excel_report/%s' % (self.id),
            'target': 'new',
        }



