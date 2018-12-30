# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)


def migrate(cr, installed_version):
    _logger.warning('Pre Migrating l10n_cl_fe from version %s to 11.0.0.5.1' % installed_version)

    cr.execute(
        "ALTER TABLE account_invoice ADD COLUMN dcn_temp INTEGER")
    cr.execute(
        "ALTER TABLE account_move ADD COLUMN dcn_temp INTEGER")
    cr.execute(
        "UPDATE account_invoice set dcn_temp=CAST(sii_document_number as Integer) where sii_document_number>0")
    cr.execute(
        "UPDATE account_move set dcn_temp=CAST(sii_document_number as Integer) where sii_document_number!=''")
