# -*- coding: utf-8 -*-
import logging
from odoo import SUPERUSER_ID, api
_logger = logging.getLogger(__name__)


def migrate(cr, installed_version):
    _logger.warning('Post Migrating l10n_cl_fe from version %s to 14.0.0.34.10' % installed_version)

    env = api.Environment(cr, SUPERUSER_ID, {})
    for r in env["account.move.consumo_folios"].search([
            ('total_boletas', '=', 0),
            ('total', '!=', 0),
        ]):
        state = r.state
        r.state = 'draft'
        r._resumenes()
        r.state = state
