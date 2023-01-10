# -*- coding: utf-8 -*-
import logging
from odoo import SUPERUSER_ID, api
_logger = logging.getLogger(__name__)


def migrate(cr, installed_version):
    _logger.warning('Post Migrating l10n_cl_fe from version %s to 14.0.0.32.5' % installed_version)

    env = api.Environment(cr, SUPERUSER_ID, {})
    for r in env["account.move.consumo_folios"].search([]):
        r._resumenes()
