# -*- coding: utf-8 -*-
import datetime
from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

date_format = "%Y-%m-%d"


class EmployeeOvertime(models.Model):
    _name = 'employee.overtime'
    _inherit = 'mail.thread'
    _rec_name = 'date'

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    date = fields.Date(string="Date",
                                 help='Date on which the overtime the employee.',
                                 track_visibility="always", required=True, readonly=True, states={'draft': [('readonly', False)],})

    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'), ('approved', 'Approved'), ('cancel', 'Rejected')],
        string='Status', default='draft', track_visibility="always")

    line_ids = fields.One2many('employee.overtime.line', 'overtime_id', 'Employee Overtime', readonly=True, states={'draft': [('readonly', False)],})

    @api.model
    def create(self, vals):
        # assigning the sequence for the record
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('employee.overtime') or _('New')
        res = super(EmployeeOvertime, self).create(vals)
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



class EmployeeOvertimeLine(models.Model):
    _name = 'employee.overtime.line'

    overtime_id = fields.Many2one('employee.overtime', 'Overtime',)

    employee_id = fields.Many2one('hr.employee', string="Employee",
                                  help='Name of the employee for whom the request is creating', required=True,)
    department_id = fields.Many2one('hr.department', string="Department",
                                    help='Department of the employee', required=True,)

    date = fields.Date(string="Date",
                                 help='Date on which the overtime the employee.',
                                 track_visibility="always", required=True,)
    start_hour= fields.Float('Start')
    end_hour= fields.Float('End')
    duration= fields.Float('Duration',compute="_compute_duration")

    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'), ('approved', 'Approved'), ('cancel', 'Rejected')],
        string='Status', default='draft', track_visibility="always")

    category = fields.Selection(
        [('hari_biasa', 'Lembur Hari Kerja'), ('hari_libur', 'Lembur Hari Libur')],
        string='Category', default='hari_biasa', track_visibility="always")

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        for l in self:
            l.department_id = l.employee_id.department_id.id

    def _compute_duration(self):

        for l in self:
            if l.end_hour and l.start_hour:
                l.duration=l.end_hour-l.start_hour