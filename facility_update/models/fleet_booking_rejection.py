# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class FleetBookingRejectionWizard(models.Model):
       
        _name = "fleet.rejection.reason"
        _inherit = ['mail.thread']
        _rec_name = 'booking_user_id'

        rejection_reason        = fields.Text(String="Vehicle booking rejection reason")
        booking_user_name       = fields.Char(string="Name of user booking")
        booking_user_id         = fields.Many2one('fleet.booking', 'Rejection Application Ref')
        bm_rejection_reason     = fields.Text(string='Reason')
        ho_rejection_reason     = fields.Text(string='Reason')
        email_recipient         = fields.Char(string='Email')
        
        
        @api.multi
        def submit_reason(self):
            if self.email_recipient:
                 body = "<html>\
                        <body><p>Vehicle Booking " + str(self.booking_user_id.vehicle_id.name) + "</p>\
                        <div style='font-family: Lucida Grande, Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF;'>"
                 
                 mail_server_ids = self.env['ir.mail_server'].search([], limit=1)
                 body += "<p>Please note that your vehicle booking has been rejected.</p>\
                                <p>with the reason stated below :.</p>\
                                <p>"+str(self.bm_rejection_reason)+"</p><br></br>\
                                <p>Please contact the administration if you have any query.</p>\
                                <p>Regards, </p>\
                                <p>NYDA</p>"
                 
                 body += "</body></html>"
                 if mail_server_ids.smtp_user:
                      email_to = self.email_recipient
                      template = self.env['mail.mail'].create({
                           'subject': 'Vehicle Booking Outcome',
                           'body_html': body,
                           'email_from': self.env.user.email or '',
                           })
                      template.write({'email_to': email_to})
          
                      template.send()
        @api.multi
        def ho_submit_reason(self):
            if self.email_recipient:
                 body = "<html>\
                        <body><p>Vehicle Booking " + str(self.booking_user_id.vehicle_id.name) + "</p>\
                        <div style='font-family: Lucida Grande, Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF;'>"
                 
                 mail_server_ids = self.env['ir.mail_server'].search([], limit=1)
                 body += "<p>Please note that your vehicle booking has been rejected.</p>\
                                <p>with the reason stated below :.</p>\
                                <p>"+str(self.ho_rejection_reason)+"</p><br></br>\
                                <p>Please contact the administration if you have any query.</p>\
                                <p>Regards, </p>\
                                <p>NYDA</p>"
                 
                 body += "</body></html>"
                 if mail_server_ids.smtp_user:
                      email_to = self.email_recipient
                      template = self.env['mail.mail'].create({
                           'subject': 'Vehicle Booking Outcome',
                           'body_html': body,
                           'email_from': self.env.user.email or '',
                           })
                      template.write({'email_to': email_to})
                      template.send()