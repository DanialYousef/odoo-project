# noinspection PyStatementEffect
{
    'name': 'Ecommerce App',
    'author': 'Danial Yousef',
    'category': '',
    'version': '16.0.0.1.0',
    'depends' : [
        'website' , 'website_sale' , 'product'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_category_inherit.xml'
    ],
    'application': True,
}