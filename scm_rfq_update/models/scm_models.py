# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class SCMRFQExtension(models.Model):
    _inherit = 'purchase.requisition'
    
    supplier_compliance_eval_update    = fields.One2many('scm.rfq.supplier.shortlist','rfq_id',
                                                         string='Suppliers Shortlist', domain=[('quotation_submitted', '=', True)])
    
    @api.onchange('csd_report')
    def _onchange_csd_supplier(self):
        for rec in self:
            rec.legal_name = rec.csd_report.LegalName
            rec.supplier_number = rec.csd_report.UniqueRegistrationReferenceNumber
            
            for cont in rec.csd_report.contacts:
                rec.name = cont.Name
                rec.surname = cont.Surname
                rec.cellphone_number = cont.CellphoneNumber
                rec.email_address = cont.EmailAddress

                break

            for cont in rec.csd_report.tax_certificate:
                rec.tax_status = cont.ValidationResponse
                
                break