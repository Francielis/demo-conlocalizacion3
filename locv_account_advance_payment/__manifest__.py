# encoding: UTF-8
{
    'name': 'Account Advanced Payment',
    'version':'13.0',
    'category': 'account',
    'summary':'Registro de Anticipo para proveedores y clientes',
    'description': '''
Registro de Anticipos para ser aplicados a las facturas de clientes y proveedores,
asi como los reversos de los mismos.
============================
Colaborador: Maria Carreno
''',
    'author': 'locv',
    'website': '',
    #data, es una lista donde se agregan todas las vistas del módulo, es decir los archivos.xml y archivos.csv.
    'data': [
             'security/ir.model.access.csv',
             'view/account_advance_payment.xml',
             'data/sequence_advance_data.xml',
             'view/res_partner_view.xml',
             'view/invoice_view.xml'
    ],
    #depends,  es una lista donde se agregan los módulos que deberían estar instalados (Módulos dependencia) para que el modulo pueda ser instalado en Odoo.
    'depends': ['base','web','mail','account'],
    'js': [],
    'css': [],
    'qweb' : [],
    #'installable': True,
    #'auto_install': False,
    'application': True,
}
