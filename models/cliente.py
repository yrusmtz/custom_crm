
from odoo import models, fields, api
import datetime

class Cliente(models.Model):
    _name = 'custom_crm.cliente'
    _description = 'cliente'

    name = fields.Char(string='Dirección')
    customer = fields.Many2one(string='Cliente', comodel_name='res.partner')
    date = fields.Datetime(string='Fecha de nacimiento')
    type = fields.Selection([('M', 'Masculino'), ('F', 'Femenino'), ('I', 'Nobinario')], string='Tipo', required=True)
    done = fields.Boolean(string='Realizada', readonly=True)
    image = fields.Binary(string='Imagen')

    def toggle_state(self):
        self.done = not self.done