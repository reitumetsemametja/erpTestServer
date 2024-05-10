# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError



class FleetBookingExtension(models.Model):
    _inherit = 'fleet.booking'

    state   = fields.Selection(selection_add=[('draft', 'Draft'),
                    ('branch_manager_approved', 'Branch Manager Approved'),
                    ('vehicle_return_approved', 'Return Approved')],string="Status")
    
    
    def return_vehicle(self):
        
        vehicle_return_id = self.env['fleet.vehicle.return'].sudo().search([('vehicle_booking_id', '=', self.id)],limit=1)

        if vehicle_return_id:
            
            return {
                'type': 'ir.actions.act_window',
                'name': 'Return Vehicle',
                'res_model': 'fleet.vehicle.return',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': (self.env.ref('facility_update.fleet_vehicle_return_form_view').id),
                'target': 'self',
                'res_id'    : vehicle_return_id.id,
                'context': {'default_vehicle_booking_id': self.id}
                }
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Return Vehicle',
                'res_model': 'fleet.vehicle.return',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': (self.env.ref('facility_update.fleet_vehicle_return_form_view').id),
                'target': 'self',
                'context': {'default_vehicle_booking_id': self.id}
                }

    
    def branch_manager_approve(self):
        
        self.state = 'branch_manager_approved'
        mail_template = self.env.ref('facility_update.fleet_bm_approval_email')
        mail_template.send_mail(self.id, force_send=True)
        
        return True
    
    def branch_manager_reject(self):

        self.state = 'rejected'
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Vehicle Rejection Reason',
            'res_model': 'fleet.rejection.reason',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('facility_update.fleet_booking_rejection_wizard_form_view').id),
            'target': 'new',
            'context': {'default_booking_user_name':self.booking_user_id.name,'default_email_recipient':self.user_id.login,'default_booking_user_id': self.id}
            }

    def head_office_reject(self):

        self.state = 'rejected'
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'HO Vehicle Rejection Reason',
            'res_model': 'fleet.rejection.reason',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('facility_update.ho_fleet_booking_rejection_wizard_form_view').id),
            'target': 'new',
            'context': {'default_booking_user_name':self.booking_user_id.name,'default_email_recipient':self.user_id.login,'default_booking_user_id': self.id}
            }
    
    @api.model
    def create(self, vals):
        vals['state'] = 'draft'
        return super(FleetBookingExtension, self).create(vals)
    

class FleetVehicleReturn(models.Model):
    
    _name = "fleet.vehicle.return"
    _inherit = ['mail.thread']
    _rec_name = 'vehicle_booking_id'

    vehicle_return_date = fields.Datetime(string="Return Date")
    vehicle_return_odometre = fields.Integer('Odometer')
    vehicle_booking_id = fields.Many2one('fleet.booking', string='Vehicle Booking ID')
    trip_end_point = fields.Char('Trip End Point')
    vehicle_inspection_done = fields.Boolean('Vehicle Inspection conducted? ')
    upload_vehicle_docs = fields.Binary(string="Upload Document")




    status   = fields.Selection([('vehicle_return_approved', 'Return Approved'),
                                              ('vehicle_return_rejected', 'Return Rejected')],string="Status")
    return_fuel_level = fields.Selection([('empty','E'), 
                                          ('half_empty', '1/4'),
                                          ('half','1/2'),
                                          ('half_full', '1/3'),
                                          ('full', 'F')], string='Fuel Level')
    
    @api.multi
    @api.onchange('vehicle_return_odometre','vehicle_booking_id.x_opening_kilometres' )
    def _get_total_distance(self):

        self.travelled_distance = self.vehicle_return_odometre - self.vehicle_booking_id.x_opening_kilometres

    travelled_distance = fields.Integer(compute=_get_total_distance, string="Total KM travelled")

    @api.constrains('vehicle_return_date')
    def _check_vehicle_return_date(self):
        for record in self:
            if record.vehicle_return_date < fields.Date.today():
                raise ValidationError("The end date cannot be set in the past")

    @api.constrains('vehicle_inspection_done')
    def _check_vehicle_inspection_done(self):
        for record in self:
            if record.vehicle_inspection_done != True:
                raise ValidationError("Please confirm that a vehicle inspection was conducted")

    def vehicle_return_approval(self):
        
        self.status = 'vehicle_return_approved'
        self.vehicle_booking_id.state = 'vehicle_return_approved'
        return True
    
    def vehicle_return_reject(self):
        
        self.status = 'vehicle_return_rejected'