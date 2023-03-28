import pytest

from app.models import ResourceModel
from tests.base_test_case import BaseTestCase


class TestResourceModel(BaseTestCase):
    @pytest.mark.model
    def test_resource_model(self):
        self.assertEqual(ResourceModel.query.count(), 1)
        result = ResourceModel.query.get(self.resource_model.id)
        self.assertTrue(hasattr(result, "id"))
        self.assertTrue(hasattr(result, "title"))
        self.assertTrue(hasattr(result, "content"))
        self.assertTrue(hasattr(result, "created"))
        self.assertTrue(hasattr(result, "modified"))
        self.assertIsNotNone(result.created)
        self.assertIsNotNone(result.modified)
