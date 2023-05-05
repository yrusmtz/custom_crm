
from odoo import models, fields, api
import datetime

class auto(models.Model):
    _name = 'custom_crm.auto'
    _description = 'auto'

    name = fields.Char(string='Modelo de auto')
    customer = fields.Many2one(string='Nombre del cliente', comodel_name='res.partner')
    date = fields.Datetime(string='Fecha de compra')
    type = fields.Selection([('W', 'Blanco'), ('B', 'Negro'), ('R', 'Rojo')], string='Tipo', required=True)
    done = fields.Boolean(string='Realizada', readonly=True)
    image = fields.Binary(string='Imagen')

    def toggle_state(self):
        self.done = not self.done