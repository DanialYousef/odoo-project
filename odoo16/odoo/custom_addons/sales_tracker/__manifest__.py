# noinspection PyStatementEffect
{
    'name': 'Sales Tracker',
    'author': 'Danial Yousef',
    'category': '',
    'version': '16.0.0.1.0',
    'depends' : [
        'base' , 'mail' , 'sale'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/base_menu_view.xml',
        'views/sale_plan_view.xml',
        'views/sales_record_view.xml',
        'report/sale_tracker_report.xml'

    ],
    'application': True,
}