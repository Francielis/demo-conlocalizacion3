# coding: utf-8
###########################################################################

import time

#from odoo.report import report_sxw
#from odoo.tools.translate import _
from odoo import models, api, _
from odoo.exceptions import UserError, Warning, ValidationError

class IvaReport(models.AbstractModel):
    _name = 'report.locv_withholding_iva.template_wh_vat'
    #_name = 'report.locv_withholding_iva.template_wh_vat'

    #_inherit = 'report.abstract_report'
    #_template = 'locv_withholding_iva.template_wh_vat'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not docids:
            raise UserError(_("Se necesita seleccionar la data a Imprimir"))
        data = {'form': self.env['account.wh.iva'].browse(docids)}
        res = dict()
        wh_iva = data['form']
        base_amount = []
        base_product = ''
        res_ali = []
        sum_base_general = 0
        sum_tax_general = 0
        sum_base_reducida = 0
        sum_tax_reducida = 0
        inv_nro_ctrl = ''
        inv_nro_fact = ''
        sum_base_additional = 0
        sum_tax_additional = 0
        if wh_iva and len(wh_iva) ==1 :
            if wh_iva.state == 'done':
                if (wh_iva.type == 'in_invoice' or wh_iva.type == 'in_refund'):
                    if wh_iva.wh_lines:
                        base_product = 0
                        total_base_product = 0
                        total_base_exent = 0
                        total_amount_product = 0
                        base_exent = ' '
                    if wh_iva.wh_lines.invoice_id.type == 'in_refund':
                        fact_afectted = str(wh_iva.wh_lines.invoice_id.ref)[14:29] if wh_iva.wh_lines.invoice_id.ref else ''
                        inv_refund = self.env['account.move'].search([('name','=', fact_afectted)])
                        inv_nro_fact = inv_refund.supplier_invoice_number
                        inv_nota = inv_refund.supplier_invoice_number
                        inv_nro_ctrl = inv_refund.nro_ctrl
                    elif wh_iva.wh_lines.invoice_id.type == 'in_invoice':
                        inv_nro_ctrl = wh_iva.wh_lines.invoice_id.nro_ctrl

                        res_ali = []
                        total_alicuota = 0

                        for line_tax in wh_iva.wh_lines.tax_line:
                            base_exent = ' '
                            base_product = 0
                            total_base_product = 0
                            total_base_exent = 0
                            total_amount_product = 0
                            base_exent = ' '
                            base_general = 0
                            tax_general = 0
                            rate_general = ''
                            base_reducida = 0
                            tax_reducida = 0
                            rate_reducida = ''
                            base_additional = 0
                            tax_additional = 0
                            rate_additional = ' '
                            if not ((line_tax.alicuota == 16) and not (line_tax.alicuota == 8) and not (line_tax.alicuota == 31)) and line_tax.alicuota == 0:
                                total_base_exent +=  line_tax.base
                                base_exent = self.separador_cifra(total_base_exent)

                            if line_tax.alicuota == 16:
                                base_general = line_tax.base
                                tax_general = line_tax.amount
                                rate_general = str(line_tax.alicuota)[0:2] + ' %'
                                sum_base_general += line_tax.base
                                sum_tax_general += line_tax.amount
                            if line_tax.alicuota == 8:
                                base_reducida = line_tax.base
                                tax_reducida = line_tax.amount
                                rate_reducida = str(line_tax.alicuota)[0:1] + ' %'
                                sum_base_reducida += line_tax.base
                                sum_tax_reducida += line_tax.amount
                            if line_tax.alicuota == 31:
                                base_additional = line_tax.base
                                tax_additional = line_tax.amount
                                rate_additional = str(line_tax.alicuota)[0:2] + ' %'
                                sum_base_additional += line_tax.base
                                sum_tax_additional += line_tax.amount

                            total_base_product += line_tax.base
                            base_product = self.separador_cifra(total_base_product)
                            total_amount_product += line_tax.amount
                            amount_product = self.separador_cifra(total_amount_product)


                            # if line_tax.alicuota and not line_tax.alicuota == 0:
                            #   total_alicuota = line_tax.alicuota
                            #   alicuota = self.separador_cifra(total_alicuota)
                            if base_general > 0:
                                base_general = self.separador_cifra(base_general)
                            else:
                                base_general = ' '
                            if tax_general > 0:
                                tax_general = self.separador_cifra(tax_general)
                            else:
                                tax_general = ''

                            ######################3
                            if base_reducida > 0:
                                base_reducida = self.separador_cifra(base_reducida)
                            else:
                                base_reducida = ' '
                            if tax_reducida >0:
                                tax_reducida = self.separador_cifra(tax_reducida)
                            else:
                                tax_reducida = ' '

                            ###################3
                            if base_additional > 0:
                                base_additional = self.separador_cifra(base_additional)
                            else:
                                base_additional = ' '
                            if tax_additional > 0:
                                tax_additional = self.separador_cifra(tax_additional)
                            else:
                                tax_additional = ''

                            base_amount.append({'base_general':base_general,
                                                'tax_general' :tax_general,
                                                'rate_general': rate_general,
                                                'base_reducida': base_reducida,
                                                'tax_reducida': tax_reducida,
                                                'rate_reducida': rate_reducida,
                                                'base_additional': base_additional,
                                                'tax_additional': tax_additional,
                                                'rate_additional': rate_additional,
                                                'base_exent': base_exent,
                                                })
                else:
                    raise UserError(_("El comprobante de Retencion de IVA se genera solo para los Proveedores"))
            else:
                raise UserError(_("La Retencion del IVA debe estar en estado Confirmado para poder generar su Comprobante"))
        else:
            raise UserError(_("Solo puede seleccionar una Retencion de IVA a la vez, Por favor Seleccione una y proceda a Imprimir"))
        partner_id = data['form'].partner_id
        if partner_id.company_type == 'person':
            if partner_id.nationality == 'V' or partner_id.nationality == 'E':
                document = str(partner_id.nationality) + str(partner_id.identification_id)
            else:
                document = str(partner_id.identification_id)
        else:
            document = partner_id.vat
        sum_base_general = self.separador_cifra(sum_base_general)
        sum_tax_general = self.separador_cifra(sum_tax_general)
        sum_base_reducida = self.separador_cifra(sum_base_reducida)
        sum_tax_reducida = self.separador_cifra(sum_tax_reducida)
        sum_base_additional = self.separador_cifra(sum_base_additional)
        sum_tax_additional = self.separador_cifra(sum_tax_additional)
        return {
            'data': data['form'],
            'model': self.env['report.locv_withholding_iva.template_wh_vat'],
            'lines': res, #self.get_lines(data.get('form')),
            #date.partner_id
            'inv_nro_ctrl': inv_nro_ctrl,
            'inv_nro_fact': inv_nro_fact,
            'document': document,
            'base_amount': base_amount,
            'base_product': base_product,
            'base_exent': base_exent,
            'alicuota': res_ali,
            'sum_base_general' : sum_base_general,
            'sum_tax_general': sum_tax_general,
            'sum_base_reducida' : sum_base_reducida,
            'sum_tax_reducida' : sum_tax_reducida,
            'sum_base_additional' : sum_base_additional,
            'sum_tax_additional': sum_tax_additional,
        }

    def separador_cifra(self,valor):
        monto = '{0:,.2f}'.format(valor).replace('.', '-')
        monto = monto.replace(',', '.')
        monto = monto.replace('-', ',')
        return  monto

    def get_period(self, date):
        if not date:
            raise Warning (_("You need date."))
        split_date = (str(date).split('-'))
        return str(split_date[1]) + '/' + str(split_date[0])

    def get_date(self, date):
        if not date:
            raise Warning(_("You need date."))
        split_date = (str(date).split('-'))
        return str(split_date[2]) + '/' + (split_date[1]) + '/' + str(split_date[0])

    def get_direction(self, partner):
        direction = ''
        direction = ((partner.street and partner.street + ', ') or '') +\
                    ((partner.street2 and partner.street2 + ', ') or '') +\
                    ((partner.city and partner.city + ', ') or '') +\
                    ((partner.state_id.name and partner.state_id.name + ',')or '')+ \
                    ((partner.country_id.name and partner.country_id.name + '') or '')
        #if direction == '':
        #    raise ValidationError ("Debe ingresar los datos de direccion en el proveedor")
            #direction = 'Sin direccion'
        return direction

    def get_tipo_doc(self, tipo=None):
        if not tipo:
            return []
        types = {'out_invoice': '1', 'in_invoice': '1', 'out_refund': '2',
                 'in_refund': '2'}
        return types[tipo]

    def get_t_type(self, doc_type=None, name=None):
        tt = ''
        if doc_type:
            if doc_type == "out_refund" or doc_type == "in_refund":
                tt = '02-COMP'
            elif name and name.find('PAPELANULADO') >= 0:
                tt = '03-ANU'
            else:
                tt = '01-REG'
        return tt



