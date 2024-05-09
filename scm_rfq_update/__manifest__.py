# coding=utf-8
{
    'name': 'Request For Quotation',

    'summary': """
       SCM update as per client's request.
    """,

    'description': """
      SCM Request for Quotation module for making the purchase process for the organisation.
    """,

    'sequence': 5,
    'author': 'National Youth Development Agency',
    'website' : 'http://www.nyda.co.za',
    'category': 'Finance - SCM',
    'version': '0.1',
    'depends': ['purchase_requisition','nyda_scm_tender'],
    'application': True,

    'data': [
        'views/scm_rfq_view_update.xml',
    ],
}
