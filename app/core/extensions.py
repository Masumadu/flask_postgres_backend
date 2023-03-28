from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from healthcheck import HealthCheck

from app.utils import GUID

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
cors = CORS()
healthcheck = HealthCheck()
db.__setattr__("GUID", GUID)
