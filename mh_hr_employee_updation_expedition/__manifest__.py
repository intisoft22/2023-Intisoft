{
    'name': 'Open HRMS Employee Info for Expedition',
    'version': '14.0.1.0.0',
    'summary': """Adding Advanced Fields In Employee Master""",
    'description': 'This module helps you to add more information in employee records.',
     'category': 'Generic Modules/Human Resources',
    'author': 'Meyrina Herawati',
    'website': 'www.rexmey.com',
    'depends': ['base','hr','hr_employee_updation','mh_hr_employee_promotion'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_view.xml',
        'views/erm_view.xml',
        'views/rm_view.xml',
        'views/dp_view.xml',
        'views/hr_promotion_view.xml',
        'reports/views/employee_report_view.xml',
    ],
    'installable': True,
    'auto_install': False
}
