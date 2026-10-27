"""Never delete users or replace existing indexes to resolve a conflict."""
import logging
from pymongo.errors import OperationFailure

logger = logging.getLogger(__name__)


def ensure_username_index(database):
    try:
        database.users.create_index('username', unique=True)
        return True
    except OperationFailure as error:
        if error.code not in (11000, 85, 86):
            raise
        logger.warning('Username unique index unavailable: duplicate data or index conflict; '
                       'new registrations are blocked. No records or indexes were changed.')
        return False


def username_index_ready(database):
    return any(list(index['key'].items()) == [('username', 1)]
               and index.get('unique') is True
               and not index.get('sparse') and not index.get('partialFilterExpression')
               for index in database.users.list_indexes())
