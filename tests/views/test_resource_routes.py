import uuid

import pytest
from flask import url_for

from app.enums import TokenTypeEnum
from tests.base_test_case import BaseTestCase


class TestResourceRoutes(BaseTestCase):
    @pytest.mark.views
    def test_create_resource(self):
        with self.client:
            response = self.client.post(
                url_for("resource.create_resource"),
                json=self.resource_test_data.create_resource,
            )
            response_data = response.json
            self.assertStatus(response, 201)
            self.assertIsInstance(response_data, dict)
            self.assertTrue(response_data)
            self.assert400(
                self.client.post(
                    url_for("resource.create_resource"),
                    json=self.resource_test_data.update_resource,
                )
            )

    @pytest.mark.views
    def test_get_all_resources(self):
        with self.client:
            response = self.client.get(
                url_for("resource.get_all_resources"),
                query_string={"page": 1, "per_page": 1},
            )
            response_data = response.json
            self.assert200(response)
            self.assertIsInstance(response_data, list)
            self.assertTrue(response_data)
            self.assertIsInstance(response_data[0], dict)

    @pytest.mark.views
    def test_get_resource(self):
        with self.client:
            response = self.client.get(
                url_for("resource.get_resource", resource_id=self.resource_model.id)
            )
            response_data = response.json
            self.assertStatus(response, 200)
            self.assertIsInstance(response_data, dict)
            self.assertTrue(response_data)

    @pytest.mark.views
    def test_update_resource(self):
        with self.client:
            response = self.client.patch(
                url_for("resource.update_resource", resource_id=self.resource_model.id),
                json=self.resource_test_data.update_resource,
                headers=self.headers,
            )
            response_data = response.json
            self.assert200(response)
            self.assertIsInstance(response_data, dict)
            self.assertTrue(response_data)
            self.assertEqual(
                self.resource_model.title,
                self.resource_test_data.update_resource.get("title"),
            )
            self.token_type = TokenTypeEnum.refresh_token.value
            self.assert400(
                self.client.patch(
                    url_for("resource.update_resource", resource_id=uuid.uuid4()),
                    headers=self.headers,
                )
            )

    @pytest.mark.views
    def test_delete_resource(self):
        with self.client:
            response = self.client.delete(
                url_for("resource.delete_resource", resource_id=self.resource_model.id),
                headers=self.headers,
            )
            self.assertStatus(response, 204)
            self.assert401(
                self.client.delete(
                    url_for("resource.delete_resource", resource_id=uuid.uuid4())
                )
            )

    @pytest.mark.views
    def test_get_access_token(self):
        with self.client:
            response = self.client.get(url_for("resource.get_access_token"))
            response_data = response.json
            self.assert200(response)
            self.assertIsInstance(response_data, dict)
            self.assertTrue(response_data)

    @pytest.mark.views
    def test_get_refresh_token(self):
        with self.client:
            self.token_type = TokenTypeEnum.refresh_token.value
            response = self.client.get(
                url_for("resource.get_refresh_token"),
                query_string={"refresh_token": self.refresh_token},
            )
            response_data = response.json
            self.assert200(response)
            self.assertIsInstance(response_data, dict)
            self.assertTrue(response_data)
