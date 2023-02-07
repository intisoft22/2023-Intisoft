{
    'name': 'Payroll for Expedition',
    'version': '14.0',
    'summary': 'Payroll for Expedition',
    'description': 'Payroll for Expedition',
    'category': 'HR',
    'author': 'Meyrina Herawati',
    'website': 'www.rexmey.com',
    'depends': ['hr','hr_payroll_community','mh_hr_employee_overtime','mh_hr_employee_overtime_payroll_fix'],
    'data': [
        'datas/payrollkurir_sequence.xml',
        'datas/payrollkuriros_sequence.xml',
        'datas/hr_payroll_category.xml',
        'datas/salary_rule_regular_os.xml',
        'datas/salary_rule_regular.xml',
        'datas/salary_rule_kurir_os.xml',
        'datas/salary_rule_kurir.xml',
        'datas/hr_payroll_data.xml',
        'views/hr_contract_view.xml',
        'views/hr_payroll_kurir_os_view.xml',
        'views/hr_payroll_kurir_view.xml',
        'views/hr_payroll_regular_view.xml',
        'views/hr_payroll_regularos_view.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False
}
