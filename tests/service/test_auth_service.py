import datetime
import uuid
from app.core.exceptions import AppException
import pytest
from app.enums import TokenTypeEnum
from tests.base_test_case import BaseTestCase
from flask import current_app


class TestAuthService(BaseTestCase):
    @pytest.mark.auth_service
    def test_get_token(self):
        with self.client:
            result = self.auth_service.get_token(user_id=str(uuid.uuid4()))
            self.assertIsInstance(result, dict)
            self.assertTrue(result)
            self.assertIn("access_token", result)
            self.assertIn("refresh_token", result)

    @pytest.mark.auth_service
    def test_refresh_token(self):
        with self.client:
            with self.assertLogs(logger=current_app.logger, level="ERROR") as log:
                with self.assertRaises(AppException.OperationError) as operation_error:
                    self.auth_service.refresh_token(
                        refresh_token=self.refresh_token
                    )
                self.assertTrue(operation_error.exception)
                self.assert400(operation_error.exception)
            self.assertTrue(log.output)
            self.assertIn("token invalid", log.output[0])
            self.token_type = TokenTypeEnum.refresh_token.value
            result = self.auth_service.refresh_token(
                refresh_token=self.refresh_token
            )
            self.assertIsInstance(result, dict)
            self.assertTrue(result)
            self.assertIn("access_token", result)
            self.assertIn("refresh_token", result)

    @pytest.mark.auth_service
    def test_generate_token(self):
        with self.client:
            result = self.auth_service.generate_token(
                user_id=str(uuid.uuid4()),
                token_type=TokenTypeEnum.access_token.value,
                expiration=datetime.datetime.utcnow()
            )
            self.assertIsInstance(result, str)
            self.assertTrue(result)

