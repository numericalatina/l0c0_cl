# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SO(models.Model):
    _inherit = "sale.order"

    acteco_ids = fields.Many2many("partner.activities", related="partner_invoice_id.acteco_ids",)
    acteco_id = fields.Many2one("partner.activities", string="Partner Activity",)
    referencia_ids = fields.One2many("sale.order.referencias", "so_id", string="Referencias de documento")


    def _prepare_invoice(self):
        vals = super(SO, self)._prepare_invoice()
        if self.acteco_id:
            vals["acteco_id"] = self.acteco_id.id
        if self._context.get('default_referencias', []):
            for r in self._context.get('default_referencias', []):
                if not self.env['sale.order.referencias'].search([
                    ('folio', '=', r[2]['origen']),
                    ('fecha_documento', '=', r[2]['fecha_documento']),
                    ('sii_referencia_TpoDocRef', '=', r[2]['sii_referencia_TpoDocRef']),
                    ('motivo', '=', r[2]['motivo']),
                ]):
                    self.env['sale.order.referencias'].create({
                        'folio': r[2]['origen'],
                        'fecha_documento': r[2]['fecha_documento'],
                        'sii_referencia_TpoDocRef': r[2]['sii_referencia_TpoDocRef'],
                        'motivo': r[2]['motivo'],
                        'so_id': self.id,
                    })
        return vals

    @api.depends("order_line.price_total")
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            if order.currency_id:
                amount_untaxed = order.currency_id.round(amount_untaxed)
                amount_tax = order.currency_id.round(amount_tax)
            order.update(
                {
                    "amount_untaxed": amount_untaxed,
                    "amount_tax": amount_tax,
                    "amount_total": amount_untaxed + amount_tax,
                }
            )


class SOL(models.Model):
    _inherit = "sale.order.line"

    @api.depends("product_uom_qty", "discount", "price_unit", "tax_id")
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        return super(SOL, self)._compute_amount()
        ''' Esto quedará aquí hasta comprobar de que la nueva forma de cálculo de odoo esté bien'''
        for line in self:
            taxes = line.tax_id.compute_all(
                line.price_unit,
                line.order_id.currency_id,
                line.product_uom_qty,
                product=line.product_id,
                partner=line.order_id.partner_shipping_id,
                discount=line.discount,
                uom_id=line.product_uom,
            )
            line.update(
                {
                    "price_tax": sum(t.get("amount", 0.0) for t in taxes.get("taxes", [])),
                    "price_total": taxes["total_included"],
                    "price_subtotal": taxes["total_excluded"],
                }
            )
