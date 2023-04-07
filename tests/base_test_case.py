import os
import uuid
from unittest.mock import patch

import fakeredis
from flask_testing import TestCase

from app import APP_ROOT, create_app, db
from app.controllers import ResourceController
from app.enums import TokenTypeEnum
from app.models import ResourceModel
from app.repositories import ResourceRepository
from app.schema import ResourceSchema
from app.services import AuthService
from config import Config
from tests.data import ResourceTestData


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app("config.TestingConfig")
        self.access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"  # noqa: E501
        self.refresh_token = self.access_token
        self.token_type = TokenTypeEnum.access_token.value
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        self.setup_patches()
        self.instantiate_classes(self.redis)
        return app

    def instantiate_classes(self, redis_service):
        self.resource_schema = ResourceSchema()
        self.resource_repository = ResourceRepository(
            redis_service=redis_service, resource_schema=self.resource_schema
        )
        self.auth_service = AuthService()
        self.resource_controller = ResourceController(
            resource_repository=self.resource_repository,
            auth_service=self.auth_service,
        )
        self.resource_test_data = ResourceTestData()

    def setup_patches(self):
        self.redis_patcher = patch(
            "app.services.redis_service.redis_conn", fakeredis.FakeStrictRedis()
        )
        self.addCleanup(self.redis_patcher.stop)
        self.redis = self.redis_patcher.start()
        jwt_decode = patch("app.utils.auth.jwt.decode", self.decoded_token)
        self.addCleanup(jwt_decode.stop)
        jwt_decode.start()
        bug_report = patch("app.core.log_config.MailHandler.send_mail")
        self.addCleanup(bug_report.stop)
        bug_report.start()

    def setUp(self):
        """
        Will be called before every test
        """
        db.create_all()
        self.resource_model = ResourceModel(**self.resource_test_data.existing_resource)
        db.session.add(self.resource_model)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()
        db.drop_all()

        file = f"{Config.SQL_DB_NAME}.sqlite3"
        file_path = os.path.join(APP_ROOT, file)
        os.remove(file_path)

    # noinspection PyMethodMayBeStatic
    def decoded_token(self, *args, **kwargs):
        return {"token_type": self.token_type, "user_id": str(uuid.uuid4())}
