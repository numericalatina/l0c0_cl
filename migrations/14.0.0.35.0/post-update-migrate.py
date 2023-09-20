import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, installed_version):
    _logger.warning("Post Migrating l10n_cl_fe from version %s to 14.0.0.35.0" % installed_version)

    env = api.Environment(cr, SUPERUSER_ID, {})
    cr.execute('''UPDATE dte_caf caf
SET document_class_id = dc.id, state = status
FROM sii_document_class dc
WHERE caf.sii_document_class = dc.sii_code''')
    cr.execute('''UPDATE ir_sequence
SET is_dte = TRUE
WHERE sii_document_class_id IS NOT NULL''')
