# -*- coding: utf-8 -*-
import logging
from odoo import SUPERUSER_ID, api
_logger = logging.getLogger(__name__)


def migrate(cr, installed_version):
    _logger.warning('Post Migrating l10n_cl_fe from version %s to 14.0.0.34.9' % installed_version)

    env = api.Environment(cr, SUPERUSER_ID, {})
    cr.execute('''update account_move set name='/'  where use_documents is FALSE AND document_class_id IS NOT NULL move_type in ('in_invoice', 'in_refund') ''')
