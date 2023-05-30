import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo import models, api, fields, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
import base64
from io import BytesIO
import xlsxwriter

class VisitFormatReportXls(models.AbstractModel):
    _name = 'report.custom_crm.custom_crm.visit'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'reporte visita en excel'

    @api.model
    def get_nomi_data_banco(self):
   
        sheet = workbook.add_worksheet(_('Formato de Banco'))
        cont+=1
        format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'vcenter', 'bold': True})
        format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        format22 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': False, 'left': False,'bottom': False, 'top': False, 'bold': False})
        format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True,'bg_color':'#ff0000','color':'#ffffff'})
        format23 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': False, 'left': False,'bottom': False, 'top': False, 'bold': True})
        format24 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': False, 'left': False,'bottom': False, 'top': False, 'bold': False})
        ########### NUMBER FORMAT #######################################
        format3 = workbook.add_format({'align':'right','left':False,'right':False,'bottom': False, 'top': False, 'font_size': 10,'num_format': '#,##0.00'})
        format4 = workbook.add_format({'align':'left','left':False,'right':False,'bottom': False, 'top': False, 'bold':False ,'font_size': 10,'num_format': '#,##0.00'})
        format5 = workbook.add_format({'align':'right','left':False,'right':False,'bottom': False, 'top': False, 'bold':True ,'font_size': 10,'num_format': 'L '+'#,##0.00'})
        font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
        red_mark = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8,
                                        'bg_color': 'red'})
        justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12})
        font_size_8.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')

        sheet.set_column(0, 0, 13)
        sheet.set_column(1, 1, 20)
        sheet.set_column(2, 2, 15)
        sheet.set_column(3, 3, 15)
        sheet.set_column(4, 4, 15)
        sheet.set_column(5, 5, 50)

        logo = self.env.user.company_id.logo
        buf_image= BytesIO(base64.b64decode(logo))
        x_scale = 0.10
        y_scale = 0.10
        #sheet.insert_image('A1', "any_name.png", {'image_data': buf_image, 'y_scale': y_scale, 'x_scale': x_scale, 'object_position':4})

        sheet.merge_range('B2:F2', company_name, format11)
        
        sheet.merge_range('B3:C3', 'Fecha Inicial: %s'%(vals.get('date_from')), format23)
        sheet.merge_range('B4:C4', 'Fecha Final: %s'%(vals.get('date_to')), format23)
        
        pos = 6
        sheet.write(5, 1, 'Identidad', format21)
        sheet.write(5, 2, 'Nombre', format21)
        sheet.write(5, 3, 'Pago Neto', format21)
        sheet.write(5, 4, 'Cuenta Bancaria', format21)
        sheet.write(5, 5, 'Descripción del Pago', format21)