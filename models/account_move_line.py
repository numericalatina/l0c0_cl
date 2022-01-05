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
            taxes_res = taxes._origin.with_context(force_sign=force_sign).compute_all(line_discount_price_unit,
                quantity=quantity, currency=currency, product=product, partner=partner, is_refund=move_type in ('out_refund', 'in_refund'),
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
        amount_total = 0
        details = dict(
            impuestos=[],
            taxInclude=False,
            MntExe=0,
            price_unit=self.price_unit,
        )
        currency_base = self.move_id.currency_base()
        for t in self.tax_ids:
            if not boleta and not nc_boleta:
                if t.sii_code in [26, 27, 28, 35, 271]:#@Agregar todos los adicionales
                    details['cod_imp_adic'] = t.sii_code
            details['taxInclude'] = t.price_include
            if t.amount == 0 or t.sii_code in [0]:#@TODO mejor manera de identificar exento de afecto
                details['IndExe'] = 1#line.product_id.ind_exe or 1
                details['MntExe'] += currency_base.round(self.price_subtotal)
            else:
                if boleta or nc_boleta:
                    amount_total += self.price_total
                amount = t.amount
                if t.sii_code in [28, 35]:
                    amount = t.compute_factor(self.product_uom_id)
                details['impuestos'].append({
                            "CodImp": t.sii_code,
                            'price_include': details['taxInclude'],
                            'TasaImp': amount,
                        }
                )
        if amount_total > 0:
            details['impuestos'].append({
                    'name': t.description,
                    "CodImp": t.sii_code,
                    'price_include': boleta or nc_boleta or details['taxInclude'],
                    'TasaImp': amount,
                }
            )
            if not details['taxInclude'] and (boleta or nc_boleta):
                taxes_res = self._get_price_total_and_subtotal_model(
                    self.price_unit,
                    1,
                    self.discount,
                    self.move_id.currency_id,
                    self.product_id,
                    self.move_id.partner_id,
                    self.tax_ids,
                    self.move_id.move_type)
                details['price_unit'] = taxes_res.get('price_total', 0.0)
        if boleta or nc_boleta:
             details['taxInclude'] = True
        return details
