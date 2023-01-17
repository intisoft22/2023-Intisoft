# -*- coding: utf-8 -*-
import datetime
from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

date_format = "%Y-%m-%d"


class EmployeePromotion(models.Model):
    _name = 'employee.promotion'
    _inherit = 'mail.thread'
    _rec_name = 'employee_id'

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string="Employee", default=lambda self: self.env.user.employee_id.id,
                                  help='Name of the employee for whom the request is creating', required=True,)
    department_id = fields.Many2one('hr.department', string="Department",
                                    help='Department of the employee', required=True,)
    promotion_date = fields.Date(string="Promotion Date",
                                 help='Date on which the promotion the employee.',
                                 track_visibility="always", required=True,)

    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'), ('approved', 'Approved'), ('cancel', 'Rejected')],
        string='Status', default='draft', track_visibility="always")

    employee_contract = fields.Many2one('hr.contract', string="Contract", required=True,)

    promotion_type = fields.Selection(
        [('Promote', 'Promote'), ('Demote', 'Demote'), ('Mutation', 'Mutation')],
        string='Type', default='Promote', track_visibility="always", required=True,)

    previous_job_id = fields.Many2one('hr.job', string="Previous Job", required=True,)
    new_job_id = fields.Many2one('hr.job', string="New Job", required=True,)
    previous_salary = fields.Float(string="Previous Salary", required=True,)
    new_salary = fields.Float(string="New Salary")
    previous_struct_id = fields.Many2one('hr.payroll.structure', string='Previous Salary Structure',)
    new_struct_id = fields.Many2one('hr.payroll.structure', string='New Salary Structure')

    change_salary = fields.Boolean(string="Change Salary?")
    read_only = fields.Boolean(string="check field")

    @api.onchange('employee_id')
    @api.depends('employee_id')
    def _compute_read_only(self):
        """ Use this function to check weather the user has the permission to change the employee"""
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        print(res_user.has_group('hr.group_hr_user'))
        if res_user.has_group('hr.group_hr_user'):
            self.read_only = True
        else:
            self.read_only = False
        self.department_id= self.employee_id.department_id.id
        self.previous_job_id= self.employee_id.job_id.id

        contract = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)],order='date_start desc')
        if contract:
            self.employee_contract=contract[0].id
            self.previous_salary=contract[0].wage
            self.previous_struct_id=contract[0].struct_id.id

    @api.model
    def create(self, vals):
        # assigning the sequence for the record
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.promotion') or _('New')
        res = super(EmployeePromotion, self).create(vals)
        return res
    

    def confirm_promotion(self):
        for rec in self:
            rec.state = 'confirm'

    def cancel_promotion(self):
        for rec in self:
            rec.state = 'cancel'

    def reject_promotion(self):
        for rec in self:
            rec.state = 'cancel'

    def reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    def approve_promotion(self):
        for rec in self:

            rec.state = 'approved'
            rec.employee_id.job_id=rec.new_job_id.id

            no_of_contract = self.env['hr.contract'].search([('employee_id', '=', rec.employee_id.id),('state','=','open')])
            if no_of_contract:
                for contract in no_of_contract:
                    contract.job_id =rec.new_job_id.id
                    if rec.change_salary:
                        contract.struct_id =rec.new_struct_id
                        contract.wage =rec.new_salary


