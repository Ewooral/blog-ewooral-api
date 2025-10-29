import reflex as rx
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import datetime
import uuid


def new_uuid() -> str:
    return str(uuid.uuid4())


class UserRoleLink(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    role_id: Optional[int] = Field(
        default=None, foreign_key="role.id", primary_key=True
    )


class RolePermissionLink(SQLModel, table=True):
    role_id: Optional[int] = Field(
        default=None, foreign_key="role.id", primary_key=True
    )
    permission_id: Optional[int] = Field(
        default=None, foreign_key="permission.id", primary_key=True
    )


class Permission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    roles: list["Role"] = Relationship(
        back_populates="permissions", link_model=RolePermissionLink
    )


class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    users: list["User"] = Relationship(back_populates="roles", link_model=UserRoleLink)
    permissions: list["Permission"] = Relationship(
        back_populates="roles", link_model=RolePermissionLink
    )


class User(SQLModel, table=True, __tablename__="user"):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=new_uuid, index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    full_name: Optional[str] = None
    phone_number: Optional[str] = Field(default=None, index=True)
    avatar_url: Optional[str] = None
    about: Optional[str] = None
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    is_business: bool = Field(default=False)
    profile_photo_privacy: str = Field(default="everyone")
    last_seen_privacy: str = Field(default="everyone")
    status_privacy: str = Field(default="contacts")
    read_receipts_enabled: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}
    )
    roles: list["Role"] = Relationship(back_populates="users", link_model=UserRoleLink)


class UserCreate(SQLModel):
    email: str
    password: str
    full_name: Optional[str] = None


class UserRead(SQLModel):
    id: int
    uuid: str
    email: str
    full_name: Optional[str] = None
    is_active: bool


class UserUpdate(SQLModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    roles: Optional[list[int]] = None