# Copyright (C) 2016 Allen Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple database migrations"""

from collections import namedtuple
import logging

from mir.sqlqs import pragma

logger = logging.getLogger(__name__)


class MigrationManager:

    """Simple database migration manager"""

    def __init__(self, initial_ver=0):
        self._migrations = {}
        self._final_ver = initial_ver

    def __repr__(self):
        cls = type(self).__qualname__
        return (f'<{cls} with migrations={self._migrations!r}'
                f' final_ver={self._final_ver!r}>')

    def register(self, migration: 'Migration'):
        """Register a migration.

        You can only register migrations in order.  For example, you can
        register migrations from version 1 to 2, then 2 to 3, then 3 to
        4.  You cannot register 1 to 2 followed by 3 to 4.
        """
        if migration.from_ver != self._final_ver:
            raise ValueError('cannot register disjoint migration')
        self._migrations[migration.from_ver] = migration
        self._final_ver = migration.to_ver

    def migration(self, from_ver: int, to_ver: int):
        """Decorator to create and register a migration.

        >>> manager = MigrationManager()
        >>> @manager.migration(0, 1)
        ... def migrate(conn):
        ...     pass
        """
        def decorator(func):
            migration = Migration(from_ver, to_ver, func)
            self.register(migration)
            return func
        return decorator

    def migrate(self, conn):
        """Migrate a database as needed.

        This method is safe to call on an up-to-date database, on an old
        database, or an uninitialized database (version 0).

        This method is idempotent.
        """
        while self.should_migrate(conn):
            self._migrate_single(conn)

    def should_migrate(self, conn) -> bool:
        """Check if database needs migration."""
        return pragma.get_user_version(conn) < self._final_ver

    def _migrate_single(self, conn):
        """Perform a single migration starting from given version."""
        self._before_migration(conn)
        with conn:
            migration = self._get_migration(pragma.get_user_version(conn))
            assert migration.from_ver == pragma.get_user_version(conn)
            logger.info('Migrating database from %d to %d',
                        migration.from_ver, migration.to_ver)
            migration.func(conn)
            self._check_foreign_keys(conn)
            pragma.set_user_version(conn, migration.to_ver)
        self._after_migration(conn)

    def _get_migration(self, version):
        try:
            return self._migrations[version]
        except KeyError:
            raise MigrationError(
                f'No registered migration for version {version}')

    def _check_foreign_keys(self, conn):
        foreign_key_errors = list(pragma.check_foreign_keys(conn))
        if foreign_key_errors:
            raise MigrationError(
                f'Foreign key check failed: {foreign_key_errors}')

    def _before_migration(self, conn):
        """Template method."""
        pragma.set_foreign_keys(conn, 0)

    def _after_migration(self, conn):
        """Template method."""
        pragma.set_foreign_keys(conn, 1)


class Migration(namedtuple('Migration', 'from_ver,to_ver,func')):

    def __new__(cls, from_ver, to_ver, func):
        if not (from_ver < to_ver):
            raise ValueError('Migration must upgrade version')
        return super().__new__(cls, from_ver, to_ver, func)


class MigrationError(Exception):
    pass
