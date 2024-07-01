from sqlalchemy import create_engine, Column, Integer, String, DateTime, UniqueConstraint, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app import db

class Account(db.Model):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    email = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    user = relationship('User', back_populates='accounts')

    __table_args__ = (
        UniqueConstraint('email', name='unique_email_accounts'),
    )

    def __init__(self, email, user_id, created_at, updated_at):
        self.uuid = uuid.uuid4()
        self.user_id = user_id
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f'<Account {self.email}>'
