# -*- coding: utf-8 -*-
{
    'name': "Facility update",

    'summary': """
        An update to the facility module to add more functionality as per end-user requirements""",

    'description': """
        Long description of module's purpose
    """,

    'author': "NYDA",
    'website': "erp.nyda.gov.za",

    'category': 'Facility',
    'version': '11.0',

    # any module necessary for this one to work correctly
    'depends': ['facility'],

    # always loaded
    'data': [
        'data/facility_update_mail_template.xml',
        'views/fleet_booking.xml',
        'views/fleet_booking_extension.xml',
        'views/fleet_vehicle_return_view.xml',
        'views/meeting_room_extension_view.xml',
        'wizard/fleet_booking_rejection.xml',

    ],
    
}