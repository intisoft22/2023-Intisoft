from datetime import datetime, timedelta
from odoo import models, fields, _, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    nik_kna = fields.Char("NIK KNA")
    code_mitra = fields.Char("Partner Code", default="KRIAN081")

    vendor_id = fields.Many2one('res.partner', 'Vendor')
    dp_id = fields.Many2many('dp.location', 'hr_employee_dp_rel', 'employee_id', 'dp_id', 'DP')
    # dp_id = fields.Many2one('dp.location', 'DP')
    joining_kna_date = fields.Date(string='KNA Joining Date', )
    divisi = fields.Char("Division", default="Region")
    status = fields.Char("Employee Status", default="Mitra Aktif")
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


class EmployeePromotion(models.Model):
    _inherit = 'employee.promotion'

    dp_id = fields.Many2many('dp.location', 'hr_promotion_dp_rel', 'employee_id', 'dp_id', 'Previous DP')
    new_dp_id = fields.Many2many('dp.location', 'hr_new_promotion_dp_rel', 'employee_id', 'dp_id', 'New DP')
    divisi = fields.Char("Division", default="Region")

    new_divisi = fields.Char("New Division", default="Region")

    @api.onchange('employee_id')
    @api.depends('employee_id')
    def _compute_read_only(self):
        """ Use this function to check weather the user has the permission to change the employee"""
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        # print(res_user.has_group('hr.group_hr_user'))
        if res_user.has_group('hr.group_hr_user'):
            self.read_only = True
        else:
            self.read_only = False
        self.department_id = self.employee_id.department_id.id
        dparray = []
        for d in self.employee_id.dp_id:
            dparray.append(d.id)
        self.dp_id = [(6, 0, dparray)]
        self.divisi = self.employee_id.divisi
        self.previous_job_id = self.employee_id.job_id.id

        contract = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)], order='date_start desc')
        if contract:
            self.employee_contract = contract[0].id
            self.previous_salary = contract[0].wage
            self.previous_struct_id = contract[0].struct_id.id

    def approve_promotion(self):
        for rec in self:
            res = super(EmployeePromotion, self).approve_promotion()
            dparray = []
            for d in rec.new_dp_id:
                dparray.append(d.id)
            rec.employee_id.dp_id = [(6, 0, dparray)]
            rec.employee_id.divisi = rec.new_divisi
            return res

class HrResignation(models.Model):
    _inherit = 'hr.resignation'
    
    def update_employee_status(self):
        resignation = self.env['hr.resignation'].search([('state', '=', 'approved')])
        for rec in resignation:
            if rec.expected_revealing_date <= fields.Date.today() and rec.employee_id.active:
                rec.employee_id.active = False
                rec.employee_id.status = "Resign"
                # Changing fields in the employee table with respect to resignation
                rec.employee_id.resign_date = rec.expected_revealing_date
                if rec.resignation_type == 'resigned':
                    rec.employee_id.resigned = True
                else:
                    rec.employee_id.fired = True
                # Removing and deactivating user
                if rec.employee_id.user_id:
                    rec.employee_id.user_id.active = False
                    rec.employee_id.user_id = None

    def approve_resignation(self):
        for rec in self:
            if rec.expected_revealing_date and rec.resign_confirm_date:
                no_of_contract = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)])
                for contracts in no_of_contract:
                    if contracts.state == 'open':
                        rec.employee_contract = contracts.name
                        rec.state = 'approved'
                        rec.approved_revealing_date = rec.resign_confirm_date + timedelta(days=contracts.notice_days)
                    else:
                        rec.approved_revealing_date = rec.expected_revealing_date
                # Changing state of the employee if resigning today
                if rec.expected_revealing_date <= fields.Date.today() and rec.employee_id.active:
                    rec.employee_id.active = False
                    rec.employee_id.status = "Resign"
                    # Changing fields in the employee table with respect to resignation
                    rec.employee_id.resign_date = rec.expected_revealing_date
                    if rec.resignation_type == 'resigned':
                        rec.employee_id.resigned = True
                    else:
                        rec.employee_id.fired = True
                    # Removing and deactivating user
                    if rec.employee_id.user_id:
                        rec.employee_id.user_id.active = False
                        rec.employee_id.user_id = None
            else:
                raise ValidationError(_('Please enter valid dates.'))