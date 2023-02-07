# -*- coding: utf-8 -*-
import datetime
from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from dateutil import relativedelta
from datetime import date, datetime, time
from pytz import timezone
from pytz import utc

date_format = "%Y-%m-%d"


class HrPayslipInput(models.Model):
    _inherit = 'hr.payslip.input'

    kurir_line_id = fields.Many2one('payroll.kuriros.line', string="Payroll Installment", help="Loan installment")
    kurir2_line_id = fields.Many2one('payroll.kurir.line', string="Payroll Installment", help="Loan installment")
    regularline_id = fields.Many2one('payroll.regularos.line', string="Payroll Installment", help="Loan installment")
    regular2line_id = fields.Many2one('payroll.regular.line', string="Payroll Installment", help="Loan installment")


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def get_inputs(self, contract_ids, date_from, date_to):
        """This Compute the other inputs to employee payslip.
                           """
        res = super(HrPayslip, self).get_inputs(contract_ids, date_from, date_to)
        day_from = datetime.combine(fields.Date.from_string(date_from), time.min)
        day_to = datetime.combine(fields.Date.from_string(date_to), time.max)

        # compute leave days
        calendar = contract_ids.resource_calendar_id
        tz = timezone(calendar.tz)
        payrollregularos_ids = self.env['payroll.regularos.line'].search(
            [('employee_id', '=', contract_ids.employee_id.id), ('date_from', '=', date_from),
             ('date_to', '=', date_to),
             ('state', '=', 'approved')])
        for regos in payrollregularos_ids:
            denda = regos.potongan
            # print(res)
            for result in res:
                if result.get('code') == 'LATEDED':
                    result['amount'] = denda
                    result['regularline_id'] = regos.id



        payrollkurir_ids = self.env['payroll.kuriros.line'].search(
            [('employee_id', '=', contract_ids.employee_id.id), ('date_from', '=', date_from),
             ('date_to', '=', date_to),
             ('state', '=', 'approved')])
        for kurir in payrollkurir_ids:
            pp_cash_intercity = kurir.pp_cash_intercity
            pp_cash_outcity = kurir.pp_cash_outcity
            pp_pm = kurir.pp_pm
            cc_cash = kurir.cc_cash
            deliv_intercity = kurir.deliv_intercity
            deliv_outcity = kurir.deliv_outcity
            denda = kurir.denda
            # print(res)
            for result in res:
                if result.get('code') == 'PPCI':
                    result['amount'] = pp_cash_intercity
                    result['kurir_line_id'] = kurir.id
                if result.get('code') == 'PPCO':
                    result['amount'] = pp_cash_outcity
                    result['kurir_line_id'] = kurir.id
                if result.get('code') == 'PPPM':
                    result['amount'] = pp_pm
                    result['kurir_line_id'] = kurir.id
                if result.get('code') == 'CCC':
                    result['amount'] = cc_cash
                    result['kurir_line_id'] = kurir.id
                if result.get('code') == 'DIC':
                    result['amount'] = deliv_intercity
                    result['kurir_line_id'] = kurir.id
                if result.get('code') == 'DOC':
                    result['amount'] = deliv_outcity
                    result['kurir_line_id'] = kurir.id
                if result.get('code') == 'DENDA':
                    result['amount'] = denda
                    result['kurir_line_id'] = kurir.id

        payrollkurir_ids = self.env['payroll.kurir.line'].search(
            [('employee_id', '=', contract_ids.employee_id.id), ('date_from', '=', date_from),
             ('date_to', '=', date_to),
             ('state', '=', 'approved')])
        for kurir in payrollkurir_ids:
            basic_salary = kurir.basic_salary
            tunjangan = kurir.tunjangan
            tambahan = kurir.tambahan
            potongan = kurir.potongan
            thr = kurir.thr
            # print(res)
            for result in res:
                if result.get('code') == 'BS':
                    result['amount'] = basic_salary
                    result['kurir2_line_id'] = kurir.id
                if result.get('code') == 'TNJ':
                    result['amount'] = tunjangan
                    result['kurir2_line_id'] = kurir.id
                if result.get('code') == 'ADD':
                    result['amount'] = tambahan
                    result['kurir2_line_id'] = kurir.id
                if result.get('code') == 'DEDK':
                    result['amount'] = potongan
                    result['kurir2_line_id'] = kurir.id
                if result.get('code') == 'THR':
                    result['amount'] = thr
                    result['kurir2_line_id'] = kurir.id
        payrollregular_ids = self.env['payroll.regular.line'].search(
            [('employee_id', '=', contract_ids.employee_id.id), ('date_from', '=', date_from),
             ('date_to', '=', date_to),
             ('state', '=', 'approved')])
        lamakerja=1
        awalkerja=contract_ids.date_start
        payslip=date_to
        selisih=payslip-awalkerja
        start_date = datetime.strptime(str(awalkerja), date_format)
        end_date = datetime.strptime(str(payslip), date_format)

        # Get the relativedelta between two dates
        delta = relativedelta.relativedelta(end_date, start_date)
        print(delta)
        print("==================================")
        if delta.months >12:
            lamakerja=12
        else:
            lamakerja=delta.months
        for regular in payrollregular_ids:
            deposit = regular.deposit
            tambahan = regular.tambahan
            insentif = regular.insentif
            potongan = regular.potongan
            thr = regular.thr
            # print(res)
            for result in res:
                if result.get('code') == 'DEP':
                    result['amount'] = deposit
                    result['regular2line_id'] = regular.id
                if result.get('code') == 'INS':
                    result['amount'] = insentif
                    result['regular2line_id'] = regular.id
                if result.get('code') == 'ADD':
                    result['amount'] = tambahan
                    result['regular2line_id'] = regular.id
                if result.get('code') == 'DEDR':
                    result['amount'] = potongan
                    result['regular2line_id'] = regular.id
                if result.get('code') == 'THRR':
                    result['amount'] = thr
                    result['regular2line_id'] = regular.id
                if result.get('code') == 'LAMAKERJA':
                    result['amount'] = lamakerja
                    result['regular2line_id'] = regular.id

        return res
