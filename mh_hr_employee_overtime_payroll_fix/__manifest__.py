{
    'name': 'Payroll overtime (fix)',
    'version': '14.0',
    'summary': 'Employee Overtime',
    'description': 'Employee Overtime',
    'category': 'HR',
    'author': 'Meyrina Herawati',
    'website': 'www.rexmey.com',
    'depends': ['hr','hr_payroll_community','mh_hr_employee_overtime'],
    'data': [
        'datas/salary_rule_overtime.xml',
        'views/hr_contract_view.xml',
        'views/employee_overtime_view.xml',
        # 'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False
}
