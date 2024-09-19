"""
Module for MotionPictures and WatchList model definitions.

This module defines the MotionPictures and WatchList models used in the Watch Wave project.
It includes relationships and constraints relevant to the application's functionality.

Classes:
    MotionPictures: Represents a motion picture (movie or series) in the Watch Wave application.
    WatchList: Represents a user's watchlist in the Watch Wave application.
"""

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
    """
    Represents a motion picture (movie or series) in the Watch Wave application.

    Attributes:
        id (int): The primary key for the motion picture.
        uuid (UUID): The universally unique identifier for the motion picture.
        title (str): The title of the motion picture.
        external_id (int): An external identifier for the motion picture.
        poster_path (str): The path to the poster image for the motion picture.
        type (str): The type of the motion picture (e.g., movie, series).
        created_at (datetime): The timestamp when the motion picture was created.
        updated_at (datetime): The timestamp when the motion picture was last updated.
        watch_list (relationship): The relationship to the WatchList model.
    """

    __tablename__ = "motion_pictures"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    title = Column(String(255), nullable=False)
    external_id = Column(Integer, nullable=False)
    poster_path = Column(String(255), nullable=False)
    overview = Column(String(255), nullable=True)
    type = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    watch_list = relationship("WatchList", back_populates="motion_picture")

    __table_args__ = (UniqueConstraint("external_id", name="unique_external_id"),)

    def __init__(
        self, title, external_id, poster_path, type, overview, created_at, updated_at
    ):
        """
        Initialize a new MotionPictures instance.

        Args:
            title (str): The title of the motion picture.
            external_id (int): An external identifier for the motion picture.
            poster_path (str): The path to the poster image for the motion picture.
            type (str): The type of the motion picture (e.g., movie, series).
            created_at (datetime): The creation timestamp.
            updated_at (datetime): The last update timestamp.
        """
        max_overview_length = 255
        if len(overview) > max_overview_length:
            overview = overview[:max_overview_length]

        self.uuid = uuid.uuid4()
        self.title = title
        self.external_id = external_id
        self.poster_path = poster_path
        self.type = type
        self.overview = overview
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        """
        Convert the MotionPictures instance to a dictionary.

        Returns:
            dict: A dictionary representation of the motion picture.
        """
        return {
            "id": self.id,
            "uuid": str(self.uuid),
            "title": self.title,
            "external_id": self.external_id,
            "poster_path": self.poster_path,
            "type": self.type,
            "overview": self.overview,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        """
        Return a string representation of the MotionPictures instance.

        Returns:
            str: A string representation of the motion picture.
        """
        return f"<MotionPictures {self.title}>"

    def __str__(self):
        """
        Return a string representation of the MotionPictures instance.

        Returns:
            str: The title of the motion picture.
        """
        return self.title


class WatchList(db.Model):
    """
    Represents a user's watchlist in the Watch Wave application.

    Attributes:
        id (int): The primary key for the watchlist item.
        account_id (int): The foreign key linking to the account.
        motion_picture_id (int): The foreign key linking to the motion picture.
        watched (bool): Indicates if the motion picture has been watched.
        created_at (datetime): The timestamp when the watchlist item was created.
        updated_at (datetime): The timestamp when the watchlist item was last updated.
        account (relationship): The relationship to the Account model.
        motion_picture (relationship): The relationship to the MotionPictures model.
    """

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
        """
        Initialize a new WatchList instance.

        Args:
            account_id (int): The ID of the associated account.
            motion_picture_id (int): The ID of the associated motion picture.
            watched (bool): Indicates if the motion picture has been watched.
            created_at (datetime): The creation timestamp.
            updated_at (datetime): The last update timestamp.
        """
        self.account_id = account_id
        self.motion_picture_id = motion_picture_id
        self.watched = watched
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        """
        Convert the WatchList instance to a dictionary.

        Returns:
            dict: A dictionary representation of the watchlist item.
        """
        return {
            "id": self.id,
            "account": self.account.to_dict() if self.account else None,
            "motion_picture": (
                self.motion_picture.to_dict() if self.motion_picture else None
            ),
            "watched": self.watched,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        """
        Return a string representation of the WatchList instance.

        Returns:
            str: A string representation of the watchlist item.
        """
        return f"<WatchList {self.id}>"

    def __str__(self):
        """
        Return a string representation of the WatchList instance.

        Returns:
            str: The ID of the watchlist item.
        """
        return str(self.id)
