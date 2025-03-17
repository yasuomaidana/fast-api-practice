from settings.database_settings import DatabaseSettings
import os
from unittest import TestCase, mock


class TestDatabaseSettings(TestCase):
    def setUp(self):
        os.environ.clear()

    def test_default_dsn(self):
        database_settings = DatabaseSettings()
        self.assertEqual(database_settings.dsn, "sqlite:///localhost")

    @mock.patch.dict(os.environ, {"DATABASE_TYPE": "postgresql"}, clear=True)
    def test_postgres_no_auth_dsn(self):
        database_settings = DatabaseSettings()
        self.assertEqual(database_settings.type, "postgresql")
        self.assertEqual(database_settings.dsn, "postgresql://localhost:5432/test")

    def test_postgres_dsn(self):
        os.environ["DATABASE_TYPE"] = "postgresql"
        os.environ["DATABASE_USER"] = "user"
        os.environ["DATABASE_PASSWORD"] = "password"
        os.environ["DATABASE_HOST"] = "host"
        os.environ["DATABASE_PORT"] = "5432"
        database_settings = DatabaseSettings()
        self.assertEqual(database_settings.dsn, "postgresql://user:password@host:5432/test")
