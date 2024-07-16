from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
    ForeignKey,
    UniqueConstraint,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app import db


class MotionPictures(db.Model):
    __tablename__ = "motion_pictures"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    title = Column(String(255), nullable=False)
    external_id = Column(Integer, nullable=False)
    poster_path = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    watch_list = relationship("WatchList", back_populates="motion_picture")

    __table_args__ = (UniqueConstraint("external_id", name="unique_external_id"),)

    def __init__(self, title, external_id, poster_path, type, created_at, updated_at):
        self.uuid = uuid.uuid4()
        self.title = title
        self.external_id = external_id
        self.poster_path = poster_path
        self.type = type
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "uuid": str(self.uuid),
            "title": self.title,
            "external_id": self.external_id,
            "poster_path": self.poster_path,
            "type": self.type,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<MotionPictures {self.title}>"

    def __str__(self):
        return f"{self.title}"


class WatchList(db.Model):
    __tablename__ = "watch_list"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    motion_picture_id = Column(
        Integer, ForeignKey("motion_pictures.id"), nullable=False
    )
    watched = Column(Boolean, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    account = relationship("Account", back_populates="watch_list")
    motion_picture = relationship("MotionPictures", back_populates="watch_list")

    def __init__(self, account_id, motion_picture_id, watched, created_at, updated_at):
        self.account_id = account_id
        self.motion_picture_id = motion_picture_id
        self.watched = watched
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "account_id": self.account_id,
            "motion_picture_id": self.motion_picture_id,
            "watched": self.watched,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<WatchList {self.id}>"

    def __str__(self):
        return f"{self.id}"
