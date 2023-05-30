# -*- coding: utf-8 -*-

import base64
from decimal import ConversionSyntax
import os
from datetime import date
from datetime import datetime
from datetime import *
import datetime
from odoo.tools.float_utils import float_round
from dateutil.relativedelta import relativedelta

from io import BytesIO
import xlsxwriter
from PIL import Image as Image
from odoo import fields, models, api, _
#from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

from xlsxwriter.utility import xl_rowcol_to_cell
import re


class payroll_report_excel_wrf(models.TransientModel):
    _name = 'report.excel.wrf'

    name = fields.Char('Archivo', size=256, readonly=True)
    file_download = fields.Binary('Descarga WRF', readonly=True)


class reporte_wrh_POS(models.Model):
    _name = "informe_pos_wrh"
    _order = 'fecha_reporte'
    _rec_name = 'fecha_reporte'

    fecha_reporte = fields.Date("Fecha", required=True)
    current_user = fields.Many2one('res.users','Current User', default=lambda self: self.env.user)

    #name = fields.Char('File Name', size=256, readonly=True)
    file_data_banco = fields.Binary('Archivo')


    @api.multi
    def validar_cierre(self):

        apunte_sesiones = self.env['pos.session'].search([('state', '=', 'opening_control')])
        if len(apunte_sesiones) >= 1:
            raise UserError(_('Para generar el informe tiene que estar cerradas todas las sesiones de los cajeros'))
            #raise ValidationError('Para generar el informe tiene que estar cerradas todas las sesiones de los cajeros')

        apunte_sesiones2 = self.env['pos.session'].search([('state', '=', 'opened')])
        if len(apunte_sesiones2) >= 1:
            raise UserError(_('Para generar el informe tiene que estar cerradas todas las sesiones de los cajeros'))

        apunte_sesiones3 = self.env['pos.session'].search([('state', '=', 'closing_control')])
        if len(apunte_sesiones3) >= 1:
            raise UserError(_('Para generar el informe tiene que estar cerradas todas las sesiones de los cajeros'))


    #ULTIMOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    @api.multi
    def get_nomi_data_banco(self):
        ini = self.fecha_reporte
        dia1 = ini.day
        mes1 = ini.month
        year1 = ini.year

        if int(dia1) < 10:
            dia1 = str(0) +''+ str(dia1)

        if int(mes1) < 10:
            mes1 = str(0) +''+ str(mes1)

        n4 = (str(dia1) +'' + str(mes1) +'' + str(year1))
        file_name = _(n4 + '-WRF')

        #Ejecuta la validacion de que todas las sesiones de los cajeros esten cerradas.
        #self.validar_cierre()


        fp = BytesIO()

        workbook = xlsxwriter.Workbook(fp)
        heading_format = workbook.add_format({'align': 'center',
                                              'valign': 'vcenter',
                                              'bold': True,
                                              'size': 12,
                                              'font_color': 'white',
                                              'bg_color' : 'red'
                                              })
        cell_text_format_n = workbook.add_format({'align': 'left',
                                                  'bold': True, 'size': 13,
                                                  })
        cell_text_format = workbook.add_format({'align': 'center',
                                                'bold': True, 'size': 9,
                                                })

        cell_text_format.set_border()
        cell_text_format_new = workbook.add_format({'align': 'center',
                                                    'size': 9,
                                                    })
        cell_text_format_new.set_border()
        cell_number_format = workbook.add_format({'align': 'center',
                                                  'bold': False, 'size': 9,
                                                  'num_format': 'L         #,##0.00'})
        cell_number_format.set_border()

        worksheet = workbook.add_worksheet('Encabezado')
        worksheet2 = workbook.add_worksheet('Detalle1')
        worksheet3 = workbook.add_worksheet('Detalle2')

        #REPORTE DE PROVEEDORES
        worksheet4 = workbook.add_worksheet('Enc Egreso')
        worksheet5 = workbook.add_worksheet('Det1 Egreso')
        worksheet6 = workbook.add_worksheet('Det2 Egreso')

        normal_num_bold = workbook.add_format({'bold': True, 'num_format': '#,###0.00', 'size': 9, })
        normal_num_bold.set_border()
        #Encabezado
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 20)
        worksheet.set_column('F:F', 20)
        worksheet.set_column('G:G', 20)
        worksheet.set_column('H:H', 20)
        worksheet.set_column('I:I', 20)
        worksheet.set_column('J:J', 20)
        worksheet.set_column('K:K', 20)
        worksheet.set_column('L:L', 20)
        worksheet.set_column('M:M', 20)
        worksheet.set_column('N:N', 20)

        #Detalle2
        worksheet2.set_column('A:A', 20)
        worksheet2.set_column('B:B', 20)
        worksheet2.set_column('C:C', 20)
        worksheet2.set_column('D:D', 20)
        worksheet2.set_column('E:E', 20)
        worksheet2.set_column('F:F', 20)
        worksheet2.set_column('G:G', 20)
        worksheet2.set_column('H:H', 20)
        worksheet2.set_column('I:I', 20)
        worksheet2.set_column('J:J', 20)
        worksheet2.set_column('K:K', 20)
        worksheet2.set_column('L:L', 20)
        worksheet2.set_column('M:M', 20)
        worksheet2.set_column('N:N', 20)
        worksheet2.set_column('O:O', 20)
        worksheet2.set_column('P:P', 20)
        worksheet2.set_column('Q:Q', 20)
        worksheet2.set_column('R:R', 20)

        #Detalle3
        worksheet3.set_column('A:A', 20)
        worksheet3.set_column('B:B', 20)
        worksheet3.set_column('C:C', 20)
        worksheet3.set_column('D:D', 20)
        worksheet3.set_column('E:E', 20)
        worksheet3.set_column('F:F', 20)
        worksheet3.set_column('G:G', 20)
        worksheet3.set_column('H:H', 20)
        worksheet3.set_column('I:I', 20)
        worksheet3.set_column('J:J', 20)
        worksheet3.set_column('K:K', 20)
        worksheet3.set_column('L:L', 20)
        worksheet3.set_column('M:M', 20)
        worksheet3.set_column('N:N', 20)
        worksheet3.set_column('O:O', 20)
        worksheet3.set_column('P:P', 20)
        worksheet3.set_column('Q:Q', 20)
        worksheet3.set_column('R:R', 20)


        #Detalle4
        worksheet4.set_column('A:A', 20)
        worksheet4.set_column('B:B', 20)
        worksheet4.set_column('C:C', 20)
        worksheet4.set_column('D:D', 20)
        worksheet4.set_column('E:E', 20)
        worksheet4.set_column('F:F', 20)
        worksheet4.set_column('G:G', 20)
        worksheet4.set_column('H:H', 20)
        worksheet4.set_column('I:I', 20)
        worksheet4.set_column('J:J', 20)
        worksheet4.set_column('K:K', 20)
        worksheet4.set_column('L:L', 20)
        worksheet4.set_column('M:M', 20)
        worksheet4.set_column('N:N', 20)
        worksheet4.set_column('O:O', 20)
        worksheet4.set_column('P:P', 20)
        worksheet4.set_column('Q:Q', 20)
        worksheet4.set_column('R:R', 20)

        worksheet5.set_column('A:A', 20)
        worksheet5.set_column('B:B', 20)
        worksheet5.set_column('C:C', 20)
        worksheet5.set_column('D:D', 20)
        worksheet5.set_column('E:E', 20)
        worksheet5.set_column('F:F', 20)
        worksheet5.set_column('G:G', 20)
        worksheet5.set_column('H:H', 20)
        worksheet5.set_column('I:I', 20)
        worksheet5.set_column('J:J', 20)
        worksheet5.set_column('K:K', 20)
        worksheet5.set_column('L:L', 20)
        worksheet5.set_column('M:M', 20)
        worksheet5.set_column('N:N', 20)
        worksheet5.set_column('O:O', 20)
        worksheet5.set_column('P:P', 20)
        worksheet5.set_column('Q:Q', 20)
        worksheet5.set_column('R:R', 20)

        worksheet6.set_column('A:A', 20)
        worksheet6.set_column('B:B', 20)
        worksheet6.set_column('C:C', 20)
        worksheet6.set_column('D:D', 20)
        worksheet6.set_column('E:E', 20)
        worksheet6.set_column('F:F', 20)
        worksheet6.set_column('G:G', 20)
        worksheet6.set_column('H:H', 20)
        worksheet6.set_column('I:I', 20)
        worksheet6.set_column('J:J', 20)
        worksheet6.set_column('K:K', 20)
        worksheet6.set_column('L:L', 20)
        worksheet6.set_column('M:M', 20)
        worksheet6.set_column('N:N', 20)
        worksheet6.set_column('O:O', 20)
        worksheet6.set_column('P:P', 20)
        worksheet6.set_column('Q:Q', 20)
        worksheet6.set_column('R:R', 20)


        #date_2 = datetime.strftime(self.date_end, '%Y-%m-%d %H:%M:%S')
        #date_1= datetime.strftime(self.from_date, '%Y-%m-%d %H:%M:%S')
        #payroll_month = self.from_date.strftime("%B")

        #worksheet.merge_range('A1:F2', 'Payroll For %s %s' % (payroll_month, self.from_date.year), heading_format)
        #INSERTAR IMAGEN DEL LOGO EN EL DOCUMENTO DE EXCEL, AMTES DE REALIZAR TIENE QUE ESTAR EL LOGO
        logo = self.env.user.company_id.logo
        buf_image= BytesIO(base64.b64decode(logo))
        x_scale = 0.43
        y_scale = 0.15
        worksheet.insert_image('A1', "any_name.png", {'image_data': buf_image, 'y_scale': y_scale, 'x_scale': x_scale, 'object_position':4})
        worksheet4.insert_image('A1', "any_name.png", {'image_data': buf_image, 'y_scale': y_scale, 'x_scale': x_scale, 'object_position':4})

        row = 2
        column = 0


        #fini = str(self.date_end)
        nombre_empre = str(self.env.user.company_id.name)
        #worksheet.merge_range('B5:D5', '%s' % (self.env.user.company_id.name), cell_text_format_n)

        #Encabezado
        worksheet.write('E1',  'Empresa',  cell_text_format_n)
        worksheet.write('F1',  nombre_empre)
        row += 1
        worksheet.write('E2', 'Fecha Inicial',  cell_text_format_n)
        worksheet.write('F2', ini)
        row += 1
        #worksheet.write('E3', 'Fecha Final', cell_text_format_n)
        #worksheet.write('F3', fini)
        worksheet4.write('E1',  'Empresa',  cell_text_format_n)
        worksheet4.write('F1',  nombre_empre)
        worksheet4.write('E2', 'Fecha Inicial',  cell_text_format_n)
        worksheet4.write('F2', ini)



        row += 2

        row = 6

        worksheet.write(row, 0, 'Emp_codigo', heading_format)
        worksheet.write(row, 1, 'Tpol_Codig', heading_format)
        worksheet.write(row, 2, 'Pol_numero', heading_format)
        worksheet.write(row, 3, 'Pol_fecha', heading_format)
        worksheet.write(row, 4, 'Pol_1Descr', heading_format)
        worksheet.write(row, 5, 'Pol_2Descr', heading_format)
        worksheet.write(row, 6, 'Pol_3Descr', heading_format)
        worksheet.write(row, 7, 'Pol_usuari', heading_format)
        worksheet.write(row, 8, 'Pol_ContLi', heading_format)
        worksheet.write(row, 9, 'Pol_Estado', heading_format)

        #Detalle1
        row1 = 0

        worksheet2.write(row1, 0, 'Emp_codigo', heading_format)
        worksheet2.write(row1, 1, 'Tpol_Codig', heading_format)
        worksheet2.write(row1, 2, 'Pol_numero', heading_format)
        worksheet2.write(row1, 3, 'Pol_linea', heading_format)
        worksheet2.write(row1, 4, 'Cat_1nivel', heading_format)
        worksheet2.write(row1, 5, 'Cat_2nivel', heading_format)
        worksheet2.write(row1, 6, 'Cat_3nivel', heading_format)
        worksheet2.write(row1, 7, 'Cat_4nivel', heading_format)
        worksheet2.write(row1, 8, 'Cat_5nivel', heading_format)
        worksheet2.write(row1, 9, 'Cat_6nivel', heading_format)
        worksheet2.write(row1, 10, 'Cat_7nivel', heading_format)
        worksheet2.write(row1, 11, 'Cat_8nivel', heading_format)
        worksheet2.write(row1, 12, 'Pol_Debe', heading_format)
        worksheet2.write(row1, 13, 'Pol_Haber', heading_format)
        worksheet2.write(row1, 14, 'Pol_DescLi', heading_format)
        worksheet2.write(row1, 15, 'Pol_dFecha', heading_format)

        #Detalle2
        worksheet3.write(row1, 0, 'Emp_codigo', heading_format)
        worksheet3.write(row1, 1, 'Tpol_Codig', heading_format)
        worksheet3.write(row1, 2, 'Pol_numero', heading_format)
        worksheet3.write(row1, 3, 'Pol_linea', heading_format)
        worksheet3.write(row1, 4, 'Age_codigo', heading_format)
        worksheet3.write(row1, 5, 'Fon_codigo', heading_format)
        worksheet3.write(row1, 6, 'Prog_codig', heading_format)
        worksheet3.write(row1, 7, 'Pol_Debe', heading_format)
        worksheet3.write(row1, 8, 'Pol_heber', heading_format)


        #PROVEEDORES
        worksheet4.write(row, 0, 'Emp_codigo', heading_format)
        worksheet4.write(row, 1, 'Tpol_Codig', heading_format)
        worksheet4.write(row, 2, 'Pol_numero', heading_format)
        worksheet4.write(row, 3, 'Pol_fecha', heading_format)
        worksheet4.write(row, 4, 'Pol_1Descr', heading_format)
        worksheet4.write(row, 5, 'Pol_2Descr', heading_format)
        worksheet4.write(row, 6, 'Pol_3Descr', heading_format)
        worksheet4.write(row, 7, 'Pol_usuari', heading_format)
        worksheet4.write(row, 8, 'Pol_ContLi', heading_format)
        worksheet4.write(row, 9, 'Pol_Estado', heading_format)

        #row1 = 0

        worksheet5.write(row1, 0, 'Emp_codigo', heading_format)
        worksheet5.write(row1, 1, 'Tpol_Codig', heading_format)
        worksheet5.write(row1, 2, 'Pol_numero', heading_format)
        worksheet5.write(row1, 3, 'Pol_linea', heading_format)
        worksheet5.write(row1, 4, 'Cat_1nivel', heading_format)
        worksheet5.write(row1, 5, 'Cat_2nivel', heading_format)
        worksheet5.write(row1, 6, 'Cat_3nivel', heading_format)
        worksheet5.write(row1, 7, 'Cat_4nivel', heading_format)
        worksheet5.write(row1, 8, 'Cat_5nivel', heading_format)
        worksheet5.write(row1, 9, 'Cat_6nivel', heading_format)
        worksheet5.write(row1, 10, 'Cat_7nivel', heading_format)
        worksheet5.write(row1, 11, 'Cat_8nivel', heading_format)
        worksheet5.write(row1, 12, 'Pol_Debe', heading_format)
        worksheet5.write(row1, 13, 'Pol_Haber', heading_format)
        worksheet5.write(row1, 14, 'Pol_DescLi', heading_format)
        worksheet5.write(row1, 15, 'Pol_dFecha', heading_format)

        worksheet6.write(row1, 0, 'Emp_codigo', heading_format)
        worksheet6.write(row1, 1, 'Tpol_Codig', heading_format)
        worksheet6.write(row1, 2, 'Pol_numero', heading_format)
        worksheet6.write(row1, 3, 'Pol_linea', heading_format)
        worksheet6.write(row1, 4, 'Age_codigo', heading_format)
        worksheet6.write(row1, 5, 'Fon_codigo', heading_format)
        worksheet6.write(row1, 6, 'Prog_codig', heading_format)
        worksheet6.write(row1, 7, 'Pol_Debe', heading_format)
        worksheet6.write(row1, 8, 'Pol_heber', heading_format)

        #Detalle1
        row1 = 0

        row_set = row
        column = 5
        #Nombre de las reglas salariales como titulo
        row = 7
        row1 = 1
        row2 = 1

        row5 = 1
        row6 = 1
        # #ENCABEZADO RELLENAR CON INFORMACION
        # apunte_conta = self.env['account.move.line'].search([('date', '=', self.fecha_reporte), ('journal_id.code', '!=', 'FACTU')])
        # #print("-----------------1:::::::::::::::::::::::::::::::::::::::::::::::::")
        # apunte_conta_pro = self.env['account.move.line'].search([('date', '=', self.fecha_reporte ),('journal_id.code', '=', 'FACTU')])
        #INV
        #FACTU

        #ENCABEZADO RELLENAR CON INFORMACION CLIENTE
        apunte_conta = self.env['account.invoice'].search([('date', '=', self.fecha_reporte), ('type', '=', 'out_invoice'),('state', '=', 'paid')])
        #print("-----------------1:::::::::::::::::::::::::::::::::::::::::::::::::")

        #ENCABEZADO RELLENAR CON INFORMACION PROVEDOR
        apunte_conta_pro = self.env['account.invoice'].search([('date', '=', self.fecha_reporte ),('type', '=', 'in_invoice'), ('state', '=', 'paid')])

        #ENCABEZADO RELLENAR CON INFORMACION DE LOS ASIENTOS GENERADOS
        apunte_sacar_entrar_dinero = self.env['account.move.line'].search([('date', '=', self.fecha_reporte), ('name', '=', 'Salida de dinero caja POS')])

        # #ENCABEZADO RELLENAR CON INFORMACION DE LOS ASIENTOS GENERADOS
        # apunte_meter_entrar_dinero = self.env['account.move.line'].search([('date', '=', self.fecha_reporte), ('name', '=', 'Motivo de dinero meter')])


        #PERDIDAS DE DINERO
        apunte_perdida_dinero = self.env['account.move.line'].search([('date', '=', self.fecha_reporte), ('name', '=', 'Diferencia de efectivo observada durante la cuenta (Pérdidas)')])

        lista_cta_clientes = {}
        lista_cta_clientes_pagos = {}
        lista_cta_provedores = {}
        lista_cta_dinero_sacar_meter = {}
        lista_cta_dinero_perdida = {}

        lista_numeros_clientes = []
        lista_numeros_clientes_pagos = []
        lista_numeros_dinero_sacar_meter = []
        lista_numeros_perddida = []

        lista_cta_clien_unica = []
        lista_cta_clien_unica_pagos = []
        lista_cta_clien_unica_sacar_meter = []
        lista_cta_clien_unica_perdida = []

        lista_cta_pro_unica = []
        lista_numeros_clientes_pro = []


        unicos_lista_clientes = []
        unicos_lista_pago_clientes = []

        unicos_lista_pro = []
        unicos_lista_pagos_pro = []

        #VARIABLE DONDE NO SE ENCUENTRAS LAS CUENTAS E ENTRADA Y SALIDA DE DINERO
        lista_no_saca_entra = []

        #VARIABLE DONDE NO SE ENCUENTRAS LAS CUENTAS DE PERDIDAS
        lista_no_perdidas = []

        acumulado = 0
        acumulado_pro = 0
        total_debi = 0
        total_credi = 0

        total_debi_pago = 0
        total_credi_pago = 0

        nombre_des = ''
        nombre_cod = ''
        lista_numeros = []
        lista_pagos = []


        total_debi = 0
        total_credi = 0

        pro_total_debi = 0
        pro_total_credi = 0
        clientes = 0
        provedores = 0

        lista_numeros_pro = []
        lista_pagos_pro = []



        pro_total_debi_pago = 0
        pro_total_credi_pago = 0

        val_perdida = ''
        val_cliente_in = ''
        val_cliente_in_pagos = ''
        val_pro_in = ''
        val_saca_mete = ''
        val_list_todo = ''

        lista_todo = []
        lista_todo_nombre = []



        #FACTURA DE PRODUCTOS
        for xx in apunte_conta:
            for pal in xx.move_id.line_ids:
                    if pal.account_id.tag_ids.display_name == '100':
                        continue
                    else:

                        lista_cta_clientes = {
                                 'total_debi': pal.debit,
                                 'total_credi': pal.credit,
                                 'nombre_des': pal.account_id.name,
                                 'catego': pal.account_id.tag_ids.display_name,
                                 'nombre_cod': pal.account_id.code }

                        lista_numeros_clientes.append(lista_cta_clientes)
                        lista_cta_clien_unica.append( pal.account_id.code)


        #OBTENGO LAS CTA UNICAS DE LOS CLIENTES
        lista_cta_clien_unica.sort()
        #Quitar duplicados
        val_cliente_in = set(lista_cta_clien_unica)


        #######################################################################################
        #INFO DE PAGO DE FACTURAS DE CLIENTES
        for pp in apunte_conta:
            for ta in pp.pos_reference:
                for lop in ta.statement_ids:
                    for pal in lop.journal_entry_ids:
                        if pal.account_id.tag_ids.display_name == '100':
                            continue
                        else:
                            #lista_numeros.append(pal.account_id.code)
                            # total_debi_pago += pal.debit
                            #total_credi_pago += pal.credit
                            # nombre_des = pal.account_id.name
                            # catego = pal.account_id.tag_ids.display_name
                            # nombre_cod = pal.account_id.code

                            lista_cta_clientes_pagos = {
                                'total_debi': pal.debit,
                                'total_credi': pal.credit,
                                'nombre_des': pal.account_id.name,
                                'catego': pal.account_id.tag_ids.display_name,
                                'nombre_cod': pal.account_id.code }

                        lista_numeros_clientes_pagos.append(lista_cta_clientes_pagos)
                        lista_cta_clien_unica_pagos.append( pal.account_id.code)

        #OBTENGO LAS CTA UNICAS DE LOS CLIENTES_PAGOS
        lista_cta_clien_unica_pagos.sort()
        #Quitar duplicados
        val_cliente_in_pagos = set(lista_cta_clien_unica_pagos)


        # print("PAGOS SIN DUPLICADOS*****************************")
        # print(val_cliente_in_pagos)

        # print("PAGOS TODOS*****************************")
        # print(lista_numeros_clientes_pagos)

        # print(aaaaaaaaaaaaaaaaa)

        ######################################################################################
        #INFO DE PROVEEDORES

        for xx in apunte_conta_pro:
            for pal in xx.move_id.line_ids:
                        lista_cta_provedores = {
                                 'total_debi': pal.debit,
                                 'total_credi': pal.credit,
                                 'nombre_des': pal.account_id.name,
                                 'catego': pal.account_id.tag_ids.display_name,
                                 'nombre_cod': pal.account_id.code }

                        lista_numeros_clientes_pro.append(lista_cta_provedores)
                        lista_cta_pro_unica.append(pal.account_id.code)


        #OBTENGO LAS CTA UNICAS DE LOS CLIENTES
        lista_cta_pro_unica.sort()
        #Quitar duplicados
        val_pro_in = set(lista_cta_pro_unica)

        # print("PROVEDOR UNICO++++++++++++++++++++++++++++++++++++++")
        # print(val_pro_in)

        # print("PROVEDOR TODA LA INFO++++++++++++++++++++++++++++++++++++++")
        # print(lista_numeros_clientes_pro)

        #####################################################################################
        #INFO DE SACAR O INGRESAR DINERO

        # print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        # print(len(apunte_sacar_entrar_dinero))

        if apunte_sacar_entrar_dinero:
            for man in apunte_sacar_entrar_dinero:
                # print("-----------------------------------------------------------------------")
                # print(kk.account_id.tag_ids.display_name)

                if man.account_id.tag_ids.display_name == '100':
                            continue
                else:
                    lista_cta_dinero_sacar_meter = {
                                'total_debi': man.debit,
                                'total_credi': man.credit,
                                'nombre_des': man.account_id.name,
                                'catego': man.account_id.tag_ids.display_name,
                                'nombre_cod': man.account_id.code }

                    # print("11111111111111111111111111111111-----//////////////////////////////////////////////////////////////////")
                    # print(lista_cta_dinero_sacar_meter)


                    lista_numeros_dinero_sacar_meter.append(lista_cta_dinero_sacar_meter)
                    lista_cta_clien_unica_sacar_meter.append(man.account_id.code)


            #OBTENGO LAS CTA UNICAS DE LOS CLIENTES
            lista_cta_clien_unica_sacar_meter.sort()
            #Quitar duplicados
            val_saca_mete = set(lista_cta_clien_unica_sacar_meter)

            # print("SACA DINERO-----------------------------------------")
            # print(lista_numeros_dinero_sacar_meter)
            # print(val_saca_mete)

        ############################################################################################
        #PERDIDA DE DINERO POR DIFERENCIAS
        if apunte_perdida_dinero:
            for pap in apunte_perdida_dinero:
                if pap.account_id.tag_ids.display_name == '100':
                            continue
                else:
                    lista_cta_dinero_perdida = {
                                'total_debi': pap.debit,
                                'total_credi': pap.credit,
                                'nombre_des': pap.account_id.name,
                                'catego': pap.account_id.tag_ids.display_name,
                                'nombre_cod': pap.account_id.code }

                    lista_numeros_perddida.append(lista_cta_dinero_perdida)
                    lista_cta_clien_unica_perdida.append(pap.account_id.code)

            #OBTENGO LAS CTA UNICAS DE LOS CLIENTES
            lista_cta_clien_unica_perdida.sort()
            #Quitar duplicados
            val_perdida = set(lista_cta_clien_unica_perdida)



        # print("INGRESAR O SACAR DINER---------------------------------------------------------------")
        # print(lista_cta_clien_unica_sacar_meter)
        # print(val_saca_in)



        #Guardar el listado de las cuentas de ese dia.

        # for patu in apunte_conta:
        #     #INFO DE PRODUCTOS
        #     for pal  in patu.move_id.line_ids:
        #         if pal.account_id.tag_ids.display_name == '100':
        #            continue
        #         else:
        #             clientes += 1
        #             lista_numeros.append(pal.account_id.code)

        #     #INFO DE PAGOS
        #     for ta in patu.pos_reference:
        #         for lop in ta.statement_ids:
        #             for pal in lop.journal_entry_ids:
        #                 print("-------------------------")
        #                 print(pal.id)
        #                 clientes += 1
        #                 #TRAIGO EL ID QUE SE GENERAR DE LOS PAGOS EN LOS ASIENTOS CONTABLES PARA LAS VENTAS DEL PUNTO DE VENTA
        #                 lista_pagos.append(pal.id)


        # lista_numeros.sort()
        # lista_pagos.sort()

        # #Quitar duplicados
        # unicos_lista = set(lista_numeros)
        # unicos_lista_pago = set(lista_pagos)


        #ENCABEZADO
        pi = self.fecha_reporte
        dia = str(pi.day)
        mes = str(pi.month)
        year = str(pi.year)
        catego = ''
        hola = ''

        if int(dia) < 10:
            dia = str(0) +''+ str(dia)

        if int(mes) < 10:
            mes = str(0) +''+ str(mes)

        n3 = (str(mes) +'' + str(dia)  +'' + str(year))

        # print("FECHA``````````````````````````````````````````````````````````````````````")
        # print(n3)


        worksheet.write(row, 0, 1, cell_text_format)
        worksheet.write(row, 1, 'IN', cell_text_format)
        worksheet.write(row, 2, n3, cell_text_format)
        worksheet.write(row, 3, str(self.fecha_reporte), cell_text_format)
        worksheet.write(row, 4, 'PARTIDA CONTABLE/INGRESOS X SERVICIOS CLINICOS', cell_text_format)
        worksheet.write(row, 5, str(hola), cell_text_format)
        worksheet.write(row, 6, str(hola), cell_text_format)
        worksheet.write(row, 7,  str(self.current_user.name), cell_text_format)
        worksheet.write(row, 9, 'E', cell_text_format)

        #PROVEEDORES
        worksheet4.write(row, 0, 1, cell_text_format)
        worksheet4.write(row, 1, 'EG', cell_text_format)
        worksheet4.write(row, 2, n3, cell_text_format)
        worksheet4.write(row, 3, str(self.fecha_reporte), cell_text_format)
        worksheet4.write(row, 4, 'PDA.EGRESOS POR SERVICIOS MEDICOS_LABORATORIO', cell_text_format)
        worksheet4.write(row, 5, str(hola), cell_text_format)
        worksheet4.write(row, 6, str(hola), cell_text_format)
        worksheet4.write(row, 7,  str(self.current_user.name), cell_text_format)
        
        worksheet4.write(row, 9, 'E', cell_text_format)

        ##################################################################################################################################
        #CLEINTES INFO
        #VALIDACION DE LOS PRODUCTOS




        if val_cliente_in:

            #INFOR DE PAGOS EN EL DEBE
            for watu in val_cliente_in:
                total_debi = 0
                total_credi = 0
                for pal in lista_numeros_clientes:
                        if watu == pal['nombre_cod']:
                            total_debi += pal['total_debi']
                            total_credi += pal['total_credi']
                            nombre_des = pal['nombre_des']
                            catego = pal['catego']
                            nombre_cod = pal['nombre_cod']



                lista_todo.append({
                                    'total_debi': total_debi,
                                    'total_credi': total_credi,
                                    'nombre_des':nombre_des,
                                    'catego': catego,
                                    'nombre_cod': nombre_cod
                                })


            # print("CLIENTE---*************************************************************")
            # print(val_cliente_in)

            # print("FACTU-CIENTES---FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
            # print(lista_todo)


        if val_cliente_in_pagos:
            # #VALIDACION DE LOS PAGOS


            for watus in val_cliente_in_pagos:

                #for natu in self.env['account.move.line'].search([('date', '=', self.fecha_reporte ), ('account_id.code', '=', watu )]):

                #INFOR DE PRODUCCTOS EN EL DHABER
                total_debi_pago = 0
                total_credi_pago = 0

                for pal in lista_numeros_clientes_pagos:
                        if watus == pal['nombre_cod']:
                            total_debi_pago += pal['total_debi']
                            total_credi_pago += pal['total_credi']
                            nombre_des = pal['nombre_des']
                            catego = pal['catego']
                            nombre_cod = pal['nombre_cod']


                #####################################################################################
                #VALIDACION PARA CUANDO SE SACA O SE METE DINERO
                if val_saca_mete:
                    for lop in val_saca_mete:
                            for tu in lista_numeros_dinero_sacar_meter:
                                if lop == tu['nombre_cod']:
                                    # print(":::::::::::::::::::::::::::::::::::::::")
                                    # print(str(tu['nombre_cod']))
                                    # print(watus)


                                    if str(tu['nombre_cod']) == watus:
                                            # total_debi_pago += tu['total_debi']
                                            # total_credi_pago += tu['total_credi']
                                            lista_no_saca_entra.append({
                                              'nombre': tu['nombre_cod']
                                             })


                #VALIDACION PARA CUANDO ES UNA PERDIDA DE DINERO
                if val_perdida:
                    for lop in val_perdida:
                            for tu in lista_numeros_perddida:
                                if lop == tu['nombre_cod']:
                                    # print(":::::::::::::::::::::::::::::::::::::::")
                                    # print(str(tu['nombre_cod']))
                                    # print(watus)


                                    if str(tu['nombre_cod']) == watus:
                                            # total_debi_pago += tu['total_debi']
                                            # total_credi_pago += tu['total_credi']
                                            lista_no_perdidas.append({
                                              'nombre': tu['nombre_cod']
                                             })


                lista_todo.append({
                    'total_debi': total_debi_pago,
                    'total_credi': total_credi_pago,
                    'nombre_des':nombre_des,
                    'catego': catego,
                    'nombre_cod': nombre_cod
                })

            # print("PAGOS-CLIENTES---FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
            # print(lista_todo)







        ###########################################################################################
        #CUENTAS NO ENCONTRADAS EN SACAR Y ENTRAD DINERO
        if val_saca_mete:

            # print("val_saca_mete************************************************************************************************")
            # print(val_saca_mete)


            # print("lista_numeros_dinero_sacar_meter************************************************************************************************")
            # print(lista_numeros_dinero_sacar_meter)

            for lopa in val_saca_mete:

                total_credi_pago_d = 0
                total_debi_pago_d = 0
                nombre_des_d = ''
                catego_d = ''
                nombre_cod_d = ''

                for tuta in lista_numeros_dinero_sacar_meter:


                    # print("NO ENTRA:::::::::::::::::::::::::::::::::::::::")
                    # print(str(tuta['nombre_cod']))
                    # print(str(lopa))

                    if lopa == tuta['nombre_cod']:
                        # for xx in lista_no_saca_entra:
                            # print(":::::::::::::::::::::::::::::::::::::::")
                            # print(str(tu['nombre_cod']))
                            # print(str(xx['nombre']))
                            # if str(tu['nombre_cod']) != str(xx['nombre']):
                        # print("2.1111111111111111111111111111/////////////////////////////////////////////////////////")
                        # print(tu['nombre_cod'])
                        # print(tu['total_debi'])
                        # print(tu['total_credi'])
                        total_debi_pago_d += tuta['total_debi']
                        total_credi_pago_d += tuta['total_credi']
                        nombre_des_d = tuta['nombre_des']
                        catego_d = tuta['catego']
                        nombre_cod_d = tuta['nombre_cod']


                if nombre_cod_d:
                    # print("222222222222222222222222222222222222222-------------------------------------------------------")

                    # print(total_credi_pago_d)
                    # print(total_debi_pago_d)

                    lista_todo.append({
                        'total_debi': total_debi_pago_d,
                        'total_credi': total_credi_pago_d,
                        'nombre_des':nombre_des_d,
                        'catego': catego_d,
                        'nombre_cod': nombre_cod_d
                    })

            # print("------------------------------************************")
            # print(lista_todo)
            # print(aaaaaaaaaaaaaaaaaaaa)


        ###################################################################################################################################
        #CUENTAS NO ENCONTRADAS EN PERDIDAS DE DINERO.
        if val_perdida:
            for lop in val_perdida:
                total_credi_pago = 0
                total_debi_pago = 0
                nombre_des = ''
                catego = ''
                nombre_cod = ''

                for tu in lista_numeros_dinero_sacar_meter:
                    if lop == tu['nombre_cod']:
                        for xx in lista_no_perdidas:

                            # print(":::::::::::::::::::::::::::::::::::::::")
                            # print(str(tu['nombre_cod']))
                            # print(watus)
                            if str(tu['nombre_cod']) != str(xx['nombre']):
                                    # print("/////////////////////////////////////////////////////////")
                                    # print(tu['nombre_cod'])
                                    # print(tu['total_debi'])

                                    total_debi_pago += tu['total_debi']
                                    total_credi_pago += tu['total_credi']
                                    nombre_des = tu['nombre_des']
                                    catego = tu['catego']
                                    nombre_cod = tu['nombre_cod']



                #DETALLE-1
                acumulado += 1

                if nombre_cod:

                    lista_todo.append({
                        'total_debi': total_debi_pago,
                        'total_credi': total_credi_pago,
                        'nombre_des':nombre_des,
                        'catego': catego,
                        'nombre_cod': nombre_cod
                    })


        ###################################################################################################################################
        if lista_todo:
            # for tt in lista_todo:
                # print("****************************************************************")
                # print(lista_todo)
                # print(aaaaaaaaaaaaaaaaaaaaaa)



                for mal in lista_todo:
                    lista_todo_nombre.append(mal['nombre_cod'])


                # print("****************************************************************")
                # print(lista_todo_nombre)

                lista_todo_nombre.sort()
                #Quitar duplicados

                val_list_todo = set(lista_todo_nombre)


                if val_list_todo:
                    for cc in val_list_todo:
                        total_debi_s = 0
                        total_credi_s = 0
                        nombre_des_s = ''
                        catego_s = ''
                        nombre_cod_s = ''

                        # print("```````````````````````````````````````````````````````````````")
                        # print(lista_todo)

                        for yu in lista_todo:
                            # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                            # print(cc)
                            # print(yu['nombre_cod'])

                            if cc == yu['nombre_cod']:
                                total_debi_s += yu['total_debi']
                                total_credi_s += yu['total_credi']
                                nombre_des_s = yu['nombre_des']
                                catego_s = yu['catego']
                                nombre_cod_s = yu['nombre_cod']

                        #DETALLE-1

                        acumulado += 1

                        worksheet2.write(row2, 0, 1, cell_text_format)
                        worksheet2.write(row2, 1, 'IN', cell_text_format)
                        worksheet2.write(row2, 2, n3, cell_text_format)
                        worksheet2.write(row2, 3,  str(acumulado), cell_text_format)

                        #Recorrido del numero de cuenta para separarlo
                        cadena = str(nombre_cod_s)
                        separador = "-"
                        resultado = cadena.split(separador)

                        worksheet2.write(row2, 4, str(resultado[0]), cell_text_format)
                        worksheet2.write(row2, 5, str(resultado[1]), cell_text_format)
                        worksheet2.write(row2, 6, str(resultado[2]), cell_text_format)
                        worksheet2.write(row2, 7, str(resultado[3]), cell_text_format)
                        worksheet2.write(row2, 8, str(resultado[4]), cell_text_format)


                        #Estos tres quedan en blanco, el numero de cuenta no es tan grande.
                        worksheet2.write(row2, 9, '0', cell_text_format)
                        worksheet2.write(row2, 10, '0', cell_text_format)
                        worksheet2.write(row2, 11, '0', cell_text_format)

                        worksheet2.write(row2, 12, total_debi_s, cell_text_format)
                        worksheet2.write(row2, 13, total_credi_s, cell_text_format)
                        worksheet2.write(row2, 14, str(nombre_des_s), cell_text_format)
                        worksheet2.write(row2, 15, str(self.fecha_reporte), cell_text_format)

                        #DETALLE 2 ARCHIVO
                        worksheet3.write(row2, 0, 1, cell_text_format)
                        worksheet3.write(row2, 1, 'IN', cell_text_format)
                        worksheet3.write(row2, 2, n3, cell_text_format)
                        worksheet3.write(row2, 3,  str(acumulado), cell_text_format)

                        if catego_s == '22':
                            worksheet3.write(row2, 4, 22, cell_text_format)
                        else:
                            worksheet3.write(row2, 4, 51, cell_text_format)

                        worksheet3.write(row2, 5, 7, cell_text_format)
                        worksheet3.write(row2, 6, 3, cell_text_format)
                        worksheet3.write(row2, 7, total_debi_s, cell_text_format)
                        worksheet3.write(row2, 8, total_credi_s, cell_text_format)


                        row2 += 1
                    worksheet.write(row, 8, str(acumulado), cell_text_format)


        ###################################################################################################################################
        #PROVEEDORES INFORMACION

        if val_pro_in:
            #VALIDACION DE LOS PRODUCTOS
            for watu in val_pro_in:

                #INFOR DE PRODUCCTOS EN EL DHABER
                pro_total_debi = 0
                pro_total_credi = 0
                for pal in lista_numeros_clientes_pro:
                        if watu == pal['nombre_cod']:
                            pro_total_debi += pal['total_debi']
                            pro_total_credi += pal['total_credi']
                            nombre_des = pal['nombre_des']
                            catego = pal['catego']
                            nombre_cod = pal['nombre_cod']
                #INFOR DE PAGOS EN EL DEBE


                #DETALLE-1
                #DETALLE-1
                acumulado_pro += 1
                n3 = (str(dia) +'' + str(mes) +'' + str(year))

                worksheet5.write(row5, 0, 1, cell_text_format)
                worksheet5.write(row5, 1, 'EG', cell_text_format)
                worksheet5.write(row5, 2, n3, cell_text_format)
                worksheet5.write(row5, 3,  str(acumulado_pro), cell_text_format)

                cadena = str(nombre_cod)
                separador = "-"
                resultado = cadena.split(separador)
                #print("index-------------------------------")
                #print(len(resultado))
                if resultado:
                    worksheet5.write(row5, 4, str(resultado[0]), cell_text_format)
                    worksheet5.write(row5, 5, str(resultado[1]), cell_text_format)
                    worksheet5.write(row5, 6, str(resultado[2]), cell_text_format)
                    worksheet5.write(row5, 7, str(resultado[3]), cell_text_format)
                    if len(resultado) > 4:
                        worksheet5.write(row5, 8, str(resultado[4]), cell_text_format)
                    else:
                        worksheet5.write(row5, 8, '', cell_text_format)

                    if len(resultado) > 5:
                        worksheet5.write(row5, 9, str(resultado[5]), cell_text_format)
                    else:
                        worksheet5.write(row5, 9, '0', cell_text_format)
                else:
                    worksheet5.write(row5, 4, '0', cell_text_format)
                    worksheet5.write(row5, 5, '0', cell_text_format)
                    worksheet5.write(row5, 6, '0', cell_text_format)
                    worksheet5.write(row5, 7, '0', cell_text_format)
                    worksheet5.write(row5, 8, '0', cell_text_format)
                    worksheet5.write(row5, 9, '0', cell_text_format)
                #worksheet5.write(row5, 8, '0', cell_text_format)
                #Estos tres quedan en blanco, el numero de cuenta no es tan grande.

                worksheet5.write(row5, 10, '0', cell_text_format)
                worksheet5.write(row5, 11, '0', cell_text_format)

                worksheet5.write(row5, 12, pro_total_debi, cell_text_format)
                worksheet5.write(row5, 13, pro_total_credi, cell_text_format)
                worksheet5.write(row5, 14, str(nombre_des), cell_text_format)
                worksheet5.write(row5, 15, str(self.fecha_reporte), cell_text_format)

                #DETALLE 3 ARCHIVO
                worksheet6.write(row5, 0, 1, cell_text_format)
                worksheet6.write(row5, 1, 'EG', cell_text_format)
                worksheet6.write(row5, 2, n3, cell_text_format)
                worksheet6.write(row5, 3,  str(acumulado_pro), cell_text_format)

                if catego == '22':
                    worksheet6.write(row5, 4, 22, cell_text_format)
                else:
                    worksheet6.write(row5, 4, 51, cell_text_format)

                worksheet6.write(row5, 5, 7, cell_text_format)
                worksheet6.write(row5, 6, 3, cell_text_format)
                worksheet6.write(row5, 7, pro_total_debi, cell_text_format)
                worksheet6.write(row5, 8, pro_total_credi, cell_text_format)
                row5 += 1


            worksheet4.write(row, 8, str(acumulado_pro), cell_text_format)


        #VALIDACION DE LOS PAGOS



        workbook.close()
        wrf_informe = base64.b64encode(fp.getvalue())
        fp.close()
        self = self.with_context(default_name=file_name, default_file_download=wrf_informe)

        return {
            'name': 'Archivo WRH',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'report.excel.wrf',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': self._context,
        }


#class PayslipBatchesWrf(models.Model):
#    _inherit = 'account.move'


