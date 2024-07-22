"""
Module for User model definition.

This module defines the User model used in the Watch Wave project.
It includes relationships and constraints relevant to the application's functionality.

Classes:
    User: Represents a user in the Watch Wave application.
"""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app import db


class User(db.Model):
    """
    Represents a user in the Watch Wave application.

    Attributes:
        id (int): The primary key for the user.
        uuid (UUID): The universally unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password_hash (str): The hashed password of the user.
        created_at (datetime): The timestamp when the user was created.
        updated_at (datetime): The timestamp when the user was last updated.
        account (relationship): The relationship to the Account model.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    account = relationship("Account", back_populates="user", uselist=False)

    __table_args__ = (UniqueConstraint("email", name="unique_email_users"),)

    def __init__(self, username, email, password_hash, created_at, updated_at):
        """
        Initialize a new User instance.

        Args:
            username (str): The username of the user.
            email (str): The email address of the user.
            password_hash (str): The hashed password of the user.
            created_at (datetime): The creation timestamp.
            updated_at (datetime): The last update timestamp.
        """
        self.uuid = uuid.uuid4()
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        """
        Convert the User instance to a dictionary.

        Returns:
            dict: A dictionary representation of the user.
        """
        return {
            "id": self.id,
            "uuid": str(self.uuid),
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        """
        Return a string representation of the User instance.

        Returns:
            str: A string representation of the user.
        """
        return f"<User {self.username}>"
