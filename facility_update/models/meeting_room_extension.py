# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta


class MeetingRoomExtension(models.Model):
    
    _inherit = 'meeting.room.booking'
    _description = "Adding more functionality to Meeting Room Booking"
    
    state               = fields.Selection(selection_add=[('rejected', 'Rejected')],
                                           string="Status")
    
    def accept_booking(self):
        
        self.state = 'accepted'
        mail_template = self.env.ref('facility_update.booking_acceptance_email')
        mail_template.send_mail(self.id, force_send=True)
        return True
    
    def reject_booking(self):
        
        self.state = 'rejected'
        mail_template = self.env.ref('facility_update.booking_rejection_email')
        mail_template.send_mail(self.id, force_send=True)
        return True