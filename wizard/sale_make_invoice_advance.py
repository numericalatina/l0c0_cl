# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"


    referencia_ids = fields.Many2many(
        'sale.order.referencias',
        string="Referencias DTE",
    )
    sale_order_ids = fields.Many2many(
        'sale.order', default=lambda self: self.env.context.get('active_ids'))

    @api.onchange('sale_order_ids')
    def set_referencias(self):
        self.referencia_ids = self.env['sale.order.referencias'].search([('so_id', 'in', self.sale_order_ids.ids)])
