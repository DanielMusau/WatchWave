"""
Module for Account model definition.

This module defines the Account model used in the Watch Wave project.
It includes relationships with User and WatchList models and enforces unique email constraints.

Classes:
    Account: Represents a user account in the Watch Wave application.
"""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    UniqueConstraint,
    func,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app import db


class Account(db.Model):
    """
    Represents a user account in the Watch Wave application.

    Attributes:
        id (int): The primary key for the account.
        uuid (UUID): The universally unique identifier for the account.
        email (str): The email address associated with the account.
        user_id (int): The foreign key linking to the user.
        created_at (datetime): The timestamp when the account was created.
        updated_at (datetime): The timestamp when the account was last updated.
        user (relationship): The relationship to the User model.
        watch_list (relationship): The relationship to the WatchList model.
    """

    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    email = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user = relationship("User", back_populates="account")
    watch_list = relationship("WatchList", back_populates="account")

    __table_args__ = (UniqueConstraint("email", name="unique_email_accounts"),)

    def __init__(self, email, user_id, created_at, updated_at):
        """
        Initialize a new Account instance.

        Args:
            email (str): The email address for the account.
            user_id (int): The ID of the associated user.
            created_at (datetime): The creation timestamp.
            updated_at (datetime): The last update timestamp.
        """
        self.uuid = uuid.uuid4()
        self.user_id = user_id
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        """
        Convert the Account instance to a dictionary.

        Returns:
            dict: A dictionary representation of the account.
        """
        return {
            "id": self.id,
            "uuid": str(self.uuid),
            "email": self.email,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        """
        Return a string representation of the Account instance.

        Returns:
            str: A string representation of the account.
        """
        return f"<Account {self.email}>"
