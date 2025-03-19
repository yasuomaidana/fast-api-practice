import os
from unittest import TestCase, mock
from pydantic import ValidationError
from settings import SecuritySettings


class TestSecuritySettings(TestCase):
    @mock.patch.dict(os.environ, {"SECURITY_ALGORITHM": "non_valid"}, clear=True)
    def test_wrong_security_settings(self):
        with self.assertRaises(ValidationError):
            SecuritySettings()

    @mock.patch.dict(os.environ, {"SECURITY_ALGORITHM": "HS512"}, clear=True)
    def test_setting_algorithm(self):
        settings = SecuritySettings()
        self.assertEqual(settings.algorithm, "HS512")
