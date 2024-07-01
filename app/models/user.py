from sqlalchemy import create_engine, Column, Integer, String, DateTime, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('email', name='unique_email_users'),
    )

    def __init__(self, username, email, password_hash, created_at, updated_at):
        self.uuid = uuid.uuid4()
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f'<User {self.username}>'
