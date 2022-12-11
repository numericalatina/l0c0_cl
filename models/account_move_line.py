# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError
from .currency import float_round_custom



class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    sequence = fields.Integer(string="Sequence", default=-1,)
    discount_amount = fields.Float(string="Monto Descuento", default=0.00,)
    is_gd_line = fields.Boolean(
        string="Es Línea descuento Global"
    )
    is_gr_line = fields.Boolean(
        string="Es Línea Recargo Global"
    )
    is_retention = fields.Boolean(
        string="ES Retención"
    )
    ind_exe = fields.Selection([
            ('1', 'No afecto o exento de IVA (10)'),
            ('2', 'Producto o servicio no es facturable'),
            ('3', 'Garantía de depósito por envases (Cervezas, Jugos, Aguas Minerales, Bebidas Analcohólicas u otros autorizados por Resolución especial)'),
            ('4', 'Ítem No Venta. (Para facturas y guías de despacho (ésta última con Indicador Tipo de Traslado de Bienes igual a 1) y este ítem no será facturado.'),
            ('5', 'Ítem a rebajar. Para guías de despacho NO VENTA que rebajan guía anterior. En el área de referencias se debe indicar la guía anterior.'),
            ('6', 'Producto o servicio no facturable negativo (excepto en liquidaciones-factura)'),
        ],
        string="Indicador Exento"
    )

    @api.onchange('tax_ids')
    def set_ind_exe(self):
        if len(self.tax_ids) == 1:
            self.ind_exe = self.tax_ids.ind_exe

    @api.onchange("discount", "price_unit", "quantity")
    def set_discount_amount(self):
        total = self.currency_id.round(self.quantity * self.price_unit)
        self.discount_amount = float_round_custom(total * ((self.discount or 0.0) / 100.0), precision_digits=0)

    @api.model
    def _get_price_total_and_subtotal_model(self, price_unit, quantity, discount, currency, product, partner, taxes, move_type, uom_id=False):
        ''' This method is used to compute 'price_total' & 'price_subtotal'.

        :param price_unit:  The current price unit.
        :param quantity:    The current quantity.
        :param discount:    The current discount.
        :param currency:    The line's currency.
        :param product:     The line's product.
        :param partner:     The line's partner.
        :param taxes:       The applied taxes.
        :param move_type:   The type of the move.
        :return:            A dictionary containing 'price_subtotal' & 'price_total'.
        '''
        res = {}

        # Compute 'price_subtotal'.
        if taxes and any(bool(t.sii_code) for t in taxes):
            line_discount_price_unit = price_unit
            total = currency.round(quantity * price_unit)
            discount_amount = float_round_custom(total * ((discount or 0.0) / 100.0), precision_digits=0)
            subtotal = quantity * line_discount_price_unit - discount_amount
        else:
            line_discount_price_unit = price_unit * (1 - (discount / 100.0))
            subtotal = quantity * line_discount_price_unit

        # Compute 'price_total'.
        if taxes:
            force_sign = -1 if move_type in ('out_invoice', 'in_refund', 'out_receipt') else 1
            taxes_res = taxes._origin.with_context(force_sign=force_sign).compute_all(
                line_discount_price_unit,
                quantity=quantity, currency=currency, product=product,
                partner=partner,
                is_refund=move_type in ('out_refund', 'in_refund'),
                discount=discount,
                uom_id=uom_id)
            res['price_subtotal'] = taxes_res['total_excluded']
            res['price_total'] = taxes_res['total_included']
        else:
            res['price_total'] = res['price_subtotal'] = subtotal
        #In case of multi currency, round before it's use for computing debit credit
        if currency:
            res = {k: currency.round(v) for k, v in res.items()}
        return res

    def get_tax_detail(self):
        boleta = self.move_id.document_class_id.es_boleta()
        nc_boleta = self.move_id.es_nc_boleta()
        details = dict(
            impuestos=[],
            taxInclude=False,
            MntExe=0,
            price_unit=self.price_unit,
            desglose=False,
        )
        currency_base = self.move_id.currency_base()
        for t in self.tax_ids:
            if self.move_id.use_documents and not self.move_id.es_nc() and \
            not self.move_id.es_nd() and self.move_id.document_class_id.sii_code \
            not in t.documentos_dte_admitidos():
                raise UserError("Tipo de documento {0} no admitido para el impuesto [{1}]{2}".format(
                    self.move_id.document_class_id.name,
                    t.sii_code,
                    t.name
                ))
            if t.es_adicional() or t.es_especifico():
                if boleta or nc_boleta:
                    continue
                details['cod_imp_adic'] = t.sii_code
            taxInclude = t.price_include and not t.sii_detailed or boleta or nc_boleta
            if len(details['impuestos']) > 0 and details['taxInclude'] != taxInclude:
                raise UserError("No puede mezclar Impuesto Incluído sin desglose e impuesto sin incluir")
            details['taxInclude'] = taxInclude
            details['desglose'] = t.sii_detailed and not boleta and not nc_boleta
            if self.ind_exe or t.ind_exe or t.amount == 0 or t.sii_code in [0]:
                details['IndExe'] = self.ind_exe or t.ind_exe or 1
                details['MntExe'] += currency_base.round(self.price_subtotal)
            else:
                amount = t.amount
                if t.sii_code in [28, 35]:
                    amount = t.compute_factor(self.product_uom_id)
                details['impuestos'].append({
                            "CodImp": t.sii_code,
                            'price_include': taxInclude,
                            'TasaImp': amount,
                            'mepco': t.mepco,
                        }
                )
        if details['desglose']:
            taxes_res = self._get_price_total_and_subtotal_model(
                    self.price_unit,
                    1,
                    0,
                    self.move_id.currency_id,
                    self.product_id,
                    self.move_id.partner_id,
                    self.tax_ids,
                    self.move_id.move_type)
            details['price_unit'] = taxes_res.get('price_subtotal', 0.0)
        return details
