# noinspection PyStatementEffect
{
    'name': 'Maintenance App',
    'author': 'Danial Yousef',
    'category': '',
    'version': '16.0.0.1.0',
    'depends' : [
        'base' ,'sale' , 'account' , 'mail' , 'web'
    ],
    'data': [
        'security\ir.model.access.csv',
        "views/base_menu.xml",
        "views/maintenance_equipment_view.xml",
        "views/maintenance_request_view.xml",
        'wizard/maintenance_change_state.xml'

    ],
    'application': True,
}