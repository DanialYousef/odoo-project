# noinspection PyStatementEffect
{
    'name': 'Todo App',
    'author': 'Danial Yousef',
    'category': '',
    'version': '16.0.0.1.0',
    'depends' : [
        'base' , 'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/todo_view.xml',
        'wizard/change_users_view.xml',
    ],
    'application': True,
}