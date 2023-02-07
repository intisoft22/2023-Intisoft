# -*- coding: utf-8 -*-
import datetime
from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from datetime import date, datetime, time
from datetime import timedelta
from dateutil.relativedelta import relativedelta
date_format = "%Y-%m-%d"



class PayrollKurir(models.Model):
    _name = 'payroll.kurir'
    _inherit = 'mail.thread'
    _rec_name = 'date_from'

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))

    date_from = fields.Date(string='Date From', readonly=True, required=True, help="Start date",
                            default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                            states={'draft': [('readonly', False)]})
    date_to = fields.Date(string='Date To', readonly=True, required=True, help="End date",
                          default=lambda self: fields.Date.to_string(
                              (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()),
                          states={'draft': [('readonly', False)]})
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'), ('approved', 'Approved'), ('cancel', 'Rejected')],
        string='Status', default='draft', track_visibility="always")

    line_ids = fields.One2many('payroll.kurir.line', 'payrollkurir_id', 'Employee', readonly=True, states={'draft': [('readonly', False)],})

    @api.model
    def create(self, vals):
        # assigning the sequence for the record
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('payroll.kurir') or _('New')
        res = super(PayrollKurir, self).create(vals)
        return res

    def confirm_overtime(self):
        for rec in self:
            rec.state = 'confirm'
            for line in rec.line_ids:
                line.state='confirm'

    def cancel_overtime(self):
        for rec in self:
            rec.state = 'cancel'
            for line in rec.line_ids:
                line.state='cancel'

    def reject_overtime(self):
        for rec in self:
            rec.state = 'cancel'
            for line in rec.line_ids:
                line.state='cancel'

    def reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'
            for line in rec.line_ids:
                line.state='draft'

    def approve_overtime(self):
        for rec in self:
            rec.state = 'approved'
            for line in rec.line_ids:
                line.state='approved'



class PayrollKurirLine(models.Model):
    _name = 'payroll.kurir.line'

    payrollkurir_id = fields.Many2one('payroll.kurir', 'Payroll',)

    employee_id = fields.Many2one('hr.employee', string="Employee",
                                  help='Name of the employee for whom the request is creating', required=True,)
    department_id = fields.Many2one('hr.department', string="Department",
                                    help='Department of the employee', required=True,)

    date_from = fields.Date(string='Date From', required=True, help="Start date",)
    date_to = fields.Date(string='Date To', required=True, help="End date",)
    basic_salary= fields.Float('Basic Salary')
    tunjangan= fields.Float('Tunjangan')
    tambahan= fields.Float('Tambahan')
    potongan= fields.Float('Potongan')
    thr= fields.Float('THR')

    employee_contract = fields.Many2one('hr.contract', string="Contract", required=True, )
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'), ('approved', 'Approved'), ('cancel', 'Rejected')],
        string='Status', default='draft', track_visibility="always")


    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        for l in self:
            contract = self.env['hr.contract'].search([('employee_id', '=', l.employee_id.id)],
                                                      order='date_start desc')
            if contract:
                l.employee_contract = contract[0].id
            l.department_id = l.employee_id.department_id.id
