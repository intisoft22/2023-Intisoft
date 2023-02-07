# -*- coding: utf-8 -*-
import datetime
from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from datetime import date, datetime, time
from pytz import timezone
from pytz import utc

date_format = "%Y-%m-%d"


class HrContractOvertime(models.Model):
    _inherit = 'hr.contract'

    typeovertime = fields.Selection([('hour', 'Hour'), ('day', 'Day')],
                                    string='type', default='hour', track_visibility="always")
    over_hour = fields.Monetary('Hour Wage')
    over_day = fields.Monetary('Day Wage')


class EmployeeOvertimeLine(models.Model):
    _inherit = 'employee.overtime.line'

    typeovertime = fields.Selection([('hour', 'Hour'), ('day', 'Day')],
                                    string='type', default='hour', track_visibility="always")
    fee_overtime = fields.Float('Fee')
    employee_contract = fields.Many2one('hr.contract', string="Contract", required=True, )

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        for l in self:
            contract = self.env['hr.contract'].search([('employee_id', '=', l.employee_id.id)],
                                                      order='date_start desc')
            if contract:
                l.employee_contract = contract[0].id
                l.typeovertime = contract[0].typeovertime
                if contract[0].typeovertime == 'hour':
                    l.fee_overtime = contract[0].over_hour
                else:

                    l.fee_overtime = contract[0].over_day
            l.department_id = l.employee_id.department_id.id


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.model
    def get_worked_day_lines(self, contracts, date_from, date_to):

        """
        @param contract: Browse record of contracts
        @return: returns a list of dict containing the input that should be applied for the given contract between date_from and date_to
        """
        res = super(HrPayslip, self).get_worked_day_lines(contracts, date_from, date_to)

        # fill only if the contract as a working schedule linked
        for contract in contracts.filtered(lambda contract: contract.resource_calendar_id):
            day_from = datetime.combine(fields.Date.from_string(date_from), time.min)
            day_to = datetime.combine(fields.Date.from_string(date_to), time.max)

            # compute leave days
            calendar = contract.resource_calendar_id
            tz = timezone(calendar.tz)
            # print(date_from)
            # print(date_to)
            overtime_ids = self.env['employee.overtime.line'].search(
                [('employee_id', '=', contract.employee_id.id), ('date', '>=', date_from), ('date', '<=', date_to),
                 ('state', '=', 'approved')])
            # print(overtime_ids)
            daysovt=0
            hourovt=0.0
            feeovt=0
            for ovt in overtime_ids:
                daysovt+=1
                hourovt+=ovt.duration
                if ovt.typeovertime == 'hour':
                    feeovt+=(ovt.fee_overtime*ovt.duration)
                else:
                    feeovt+=(ovt.fee_overtime*ovt.duration)

            overtimes = {
                'name': _("Overtime"),
                'sequence': 1,
                'code': 'OVTFIX',
                'number_of_days': daysovt,
                'number_of_hours': hourovt,
                'contract_id': contract.id,
            }

            res.append(overtimes)

        return res

    def get_inputs(self, contract_ids, date_from, date_to):
        """This Compute the other inputs to employee payslip.
                           """
        res = super(HrPayslip, self).get_inputs(contract_ids, date_from, date_to)
        day_from = datetime.combine(fields.Date.from_string(date_from), time.min)
        day_to = datetime.combine(fields.Date.from_string(date_to), time.max)

        # compute leave days
        calendar = contract_ids.resource_calendar_id
        tz = timezone(calendar.tz)

        overtime_ids = self.env['employee.overtime.line'].search(
            [('employee_id', '=', contract_ids.employee_id.id), ('date', '>=', date_from), ('date', '<=', date_to),
             ('state', '=', 'approved')])
        daysovt = 0
        hourovt = 0.0
        feeovt = 0
        for ovt in overtime_ids:
            daysovt += 1
            hourovt += ovt.duration
            # print(ovt.typeovertime)
            if ovt.typeovertime == 'hour':
                feeovt += (ovt.fee_overtime * ovt.duration)
            else:
                feeovt += (ovt.fee_overtime *1)
        # print(res)
        for result in res:
            if result.get('code') == 'OVTFIX':
                result['amount'] = feeovt
                result['contract_id'] = contract_ids.id
        return res
