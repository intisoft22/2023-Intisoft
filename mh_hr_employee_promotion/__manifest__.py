{
    'name': 'Employee Promotion',
    'version': '14.0',
    'summary': 'Employee promotion',
    'description': 'Employee promotion',
    'category': 'HR',
    'author': 'Meyrina Herawati',
    'website': 'www.rexmey.com',
    'depends': ['hr','hr_payroll_community'],
    'data': [
        'data/promotion_sequence.xml',
        'views/employee_promotion_view.xml',
        'security/ir.model.access.csv'],
    'installable': True,
    'auto_install': False
}
