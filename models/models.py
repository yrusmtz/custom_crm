# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

import io
import json
import base64
import xlsxwriter

import logging

_logger = logging.getLogger(__name__)

class Visit(models.Model):
    _name = 'custom_crm.visit'
    _description = 'Visit'

    name = fields.Char(string='Descripción')
    customer = fields.Many2one(string='Cliente', comodel_name='res.partner')
    date = fields.Datetime(string='Fecha')
    type = fields.Selection([('P', 'Presencial'), ('W', 'WhatsApp'), ('T', 'Telefónico')], string='Tipo', required=True)
    done = fields.Boolean(string='Realizada', readonly=True)
    image = fields.Binary(string='Imagen')


    def toggle_state(self):
        self.done = not self.done

    
    




        class VisitReport(models.AbstractModel):

            name='report.custom_crm.report_visit_card'

        @api.model
        def _get_report_values(self, docids, data=None):
            report_obj = self.env['ir.actions.report']
            report = report_obj._get_report_from_name('custom_crm.report_visit_card')

            return {
                'doc_ids': docids,
                'doc_model': self.env['custom_crm.visit'],
                'docs': self.env['custom_crm.visit'].browse(docids)
            }

       