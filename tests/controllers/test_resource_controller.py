import uuid

import pytest
from flask import current_app

from app.core import Result
from app.core.exceptions import AppException
from app.enums import TokenTypeEnum
from app.models import ResourceModel
from tests.base_test_case import BaseTestCase


class TestResourceController(BaseTestCase):
    @pytest.mark.controller
    def test_create_resource(self):
        result = self.resource_controller.create_resource(
            obj_data=self.resource_test_data.create_resource
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Result)
        self.assertStatus(result, 201)
        self.assertIsInstance(result.value, ResourceModel)

    @pytest.mark.controller
    def test_get_all_resource(self):
        result = self.resource_controller.get_all_resources(
            query_param={"page": 1, "per_page": 5}
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Result)
        self.assert200(result)
        self.assertIsInstance(result.value, list)
        self.assertTrue(result.value)
        self.assertIsInstance(result.value[0], ResourceModel)

    @pytest.mark.controller
    def test_get_resource(self):
        result = self.resource_controller.get_resource(obj_id=self.resource_model.id)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Result)
        self.assert200(result)
        self.assertIsInstance(result.value, ResourceModel)
        with self.assertLogs(logger=current_app.logger, level="ERROR") as logs:
            with self.assertRaises(AppException.NotFoundException) as not_found:
                self.resource_controller.get_resource(obj_id=uuid.uuid4())
            self.assertTrue(not_found.exception)
            self.assert404(not_found.exception)
        self.assertTrue(logs.output)
        self.assertIn("does not exist", logs.output[0])

    @pytest.mark.controller
    def test_update_resource(self):
        result = self.resource_controller.update_resource(
            obj_id=self.resource_model.id,
            obj_in=self.resource_test_data.update_resource,
        )
        self.assertIsNotNone(result)
        self.assert200(result)
        self.assertIsInstance(result, Result)
        self.assertIsInstance(result.value, ResourceModel)
        self.assertEqual(
            result.value.title, self.resource_test_data.update_resource.get("title")
        )
        with self.assertLogs(logger=current_app.logger, level="ERROR") as logs:
            with self.assertRaises(AppException.NotFoundException) as not_found:
                self.resource_controller.update_resource(
                    obj_id=uuid.uuid4(), obj_in=self.resource_test_data.update_resource
                )
            self.assertTrue(not_found.exception)
            self.assert404(not_found.exception)
        self.assertTrue(logs.output)
        self.assertIn("does not exist", logs.output[0])

    @pytest.mark.controller
    def test_delete_resource(self):
        result = self.resource_controller.delete_resource(obj_id=self.resource_model.id)
        self.assertIsNotNone(result)
        self.assertStatus(result, 204)
        self.assertIsNone(result.value)
        with self.assertLogs(logger=current_app.logger, level="ERROR") as logs:
            with self.assertRaises(AppException.NotFoundException) as not_found:
                self.resource_controller.delete_resource(obj_id=self.resource_model.id)
            self.assertTrue(not_found.exception)
            self.assert404(not_found.exception)
        self.assertTrue(logs.output)
        self.assertIn("does not exist", logs.output[0])

    @pytest.mark.controller
    def test_get_token(self):
        result = self.resource_controller.get_token()
        self.assertIsNotNone(result)
        self.assert200(result)
        self.assertIsInstance(result.value, dict)
        self.assertTrue(result.value)

    @pytest.mark.controller
    def test_refresh_token(self):
        self.token_type = TokenTypeEnum.refresh_token.value
        result = self.resource_controller.get_refresh_token(
            query_params={"refresh_token": self.refresh_token}
        )
        self.assertIsNotNone(result)
        self.assert200(result)
        self.assertIsInstance(result.value, dict)
        self.assertTrue(result.value)
