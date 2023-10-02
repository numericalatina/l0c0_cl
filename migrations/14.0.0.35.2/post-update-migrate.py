from odoo import SUPERUSER_ID, api
import logging


_logger = logging.getLogger(__name__)


def migrate(cr, installed_version):
    _logger.warning("Post Migrating l10n_cl_fe from version %s to 14.0.0.35.2" % installed_version)

    env = api.Environment(cr, SUPERUSER_ID, {})
    for r in env['dte.caf'].search([]):
        r.load_caf()
