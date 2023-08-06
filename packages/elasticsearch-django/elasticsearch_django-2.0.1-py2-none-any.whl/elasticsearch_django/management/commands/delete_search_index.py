# -*- coding: utf-8 -*-
"""Delete a search index (and all documents therein)."""
import logging

from elasticsearch_django.management.commands import BaseSearchCommand
from elasticsearch_django.index import delete_index

logger = logging.getLogger(__name__)


class Command(BaseSearchCommand):

    """Delete search index."""

    help = "Clears out the specified (or all) search index completely."
    description = "Delete search index"

    def do_index_command(self, index, **options):
        """Delete search index."""
        if options['interactive']:
            logger.warn("This will permanently delete the index '%s'.", index)
            if not self._confirm_action():
                logger.warn("Aborting deletion of index '%s' at user's request.", index)
                return
        return delete_index(index)
