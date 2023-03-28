import pytest

from tests.base_test_case import BaseTestCase


class TestAppConfig(BaseTestCase):
    @pytest.mark.app
    def test_app_config(self):
        self.assertTrue(self.create_app().config["DEBUG"])
        self.assertTrue(self.create_app().config["TESTING"])
        self.assertTrue(self.create_app().config["DEVELOPMENT"])
        self.assertIsNotNone(self.create_app().config["SECRET_KEY"])
