# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class AccountingReport(models.TransientModel):
    _inherit = "accounting.report"
    _description = "Account Report"

    def check_report_excel(self):
        # redirect ke controller /sale/excel_report untuk generate file excel
        return {
            'type': 'ir.actions.act_url',
            'url': '/accounting_excel_reports/excel_report/%s' % (self.id),
            'target': 'new',
        }

