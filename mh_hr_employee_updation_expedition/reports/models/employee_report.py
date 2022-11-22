# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _

from datetime import datetime, timedelta, date
from pytz import timezone
import time


class EmployeeReportWizard(models.TransientModel):
    _name = 'employee.report.wizard'

    def get_excel_report(self):
        # redirect ke controller /sale/excel_report untuk generate file excel
        return {
            'type': 'ir.actions.act_url',
            'url': '/employee/excel_report/%s' % (self.id),
            'target': 'new',
        }



