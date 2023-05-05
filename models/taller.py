from odoo import models, fields, api
import datetime


class taller(models.Model):
    _name = 'custom_crm.taller'
    _description = 'taller'

    name = fields.Char(string='Direccion del taller')
    customer = fields.Many2one(string='Usuario', comodel_name='res.partner')
    date = fields.Datetime(string='Fecha de reparacion')
    type = fields.Selection([('P', 'Presencial'), ('D', 'Domicilio'), ('C', 'Cotizacion')], string='Tipo', required=True)
    done = fields.Boolean(string='Realizada', readonly=True)
    image = fields.Binary(string='Imagen')

    def toggle_state(self):
        self.done = not self.done