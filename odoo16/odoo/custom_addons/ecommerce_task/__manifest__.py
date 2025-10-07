# noinspection PyStatementEffect
{
    'name': 'Ecommerce Task',
    'author': 'Danial Yousef',
    'category': '',
    'version': '16.0.0.1.0',
    'depends' : [
        'base' , 'product' , 'website_sale' , 'stock' ,'sale' , 'website_sale' ,'web'
    ],
    'data': [
        'views/base_menu.xml',
        'views/discount_view.xml',
        'views/vendor_view.xml',
        'views/product_view.xml',
        'views/category.xml',
        "views/pricelist_view.xml"



    ],
    'application': True,
}