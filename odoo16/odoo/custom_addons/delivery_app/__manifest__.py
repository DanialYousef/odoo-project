# noinspection PyStatementEffect
{
    'name': 'Delivery App',
    'author': 'Danial Yousef',
    'category': '',
    'version': '16.0.0.1.0',
    'depends' : [
        'base' ,'sale' , 'account' , 'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/restaurant_menu_view.xml',
        'views/restaurant_view.xml',
        'views/restaurant_address_view.xml',
        'views/users_view.xml',
        'views/delivery_order_view.xml',
        'views/res_users.xml',




    ],
    'application': True,
}