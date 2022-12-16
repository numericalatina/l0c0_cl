# -*- coding: utf-8 -*-
import logging
from odoo import SUPERUSER_ID, api
_logger = logging.getLogger(__name__)


def migrate(cr, installed_version):
    _logger.warning('Post Migrating l10n_cl_dte_point_of_sale from version %s to 14.0.0.34.9' % installed_version)

    env = api.Environment(cr, SUPERUSER_ID, {})
    for r in env["account.move"].search([
            ('use_documents', '=', False),
            ('document_class_id', '!=', False),
            ('move_type', 'in', ['in_invoice', 'in_refund'])
        ]):
        r.name = ''
        r._compute_name()
