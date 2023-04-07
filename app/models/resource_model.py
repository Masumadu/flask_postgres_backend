import datetime
import uuid
from dataclasses import dataclass

from sqlalchemy.sql import func

from app import db


@dataclass
class ResourceModel(db.Model):

    id: str
    title: str
    content: str
    created: datetime.datetime
    modified: datetime.datetime

    __tablename__ = "resources"
    id = db.Column(db.GUID(), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(), nullable=False)
    content = db.Column(db.String(), nullable=False)
    created = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    modified = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
