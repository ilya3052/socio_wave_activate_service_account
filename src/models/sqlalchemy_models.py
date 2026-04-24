from datetime import datetime
from typing import Annotated, Optional

from sqlalchemy import String, text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

str_11 = Annotated[str, 11]
str_16 = Annotated[str, 16]
str_32 = Annotated[str, 32]
str_128 = Annotated[str, 128]
str_256 = Annotated[str, 256]
str_512 = Annotated[str, 512]


class Base(DeclarativeBase):
    id: Mapped[int_pk]
    repr_cols_num = 3
    repr_columns = ()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_columns or idx < self.repr_cols_num:
                cols.append(f"{col} = {getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class TypesMixin:
    type_annotation_map = {
        str_16: String(16),
        str_32: String(32),
        str_128: String(128),
        str_256: String(256),
        str_512: String(512)
    }


class PlatformModel(Base, TypesMixin):
    __tablename__ = "social_entities_platform"

    name: Mapped[str_128]


class ServiceAccountModel(Base, TypesMixin):
    __tablename__ = "service_accounts_serviceaccount"
    name: Mapped[str_128]
    platform_id: Mapped[int] = mapped_column(ForeignKey("social_entities_platform.id", ondelete="CASCADE"))
    app_id: Mapped[Optional[int]] = mapped_column(unique=True, nullable=True)
    is_activated: Mapped[bool] = mapped_column(server_default=text('false'))
    data: Mapped['ServiceAccountDataModel'] = relationship(
        uselist=False,
        back_populates='serviceAccount'
    )


class ServiceAccountDataModel(Base, TypesMixin):
    __tablename__ = "service_accounts_serviceaccountdata"

    service_key: Mapped[Optional[str_256]]
    protected_key: Mapped[Optional[str_256]]
    phone_number: Mapped[Optional[str_11]]
    session_path: Mapped[Optional[str_256]]

    account_id: Mapped[int] = mapped_column(ForeignKey("service_accounts_serviceaccount.id", ondelete='CASCADE'))
    serviceAccount: Mapped['ServiceAccountModel'] = relationship(back_populates='data')


class UserModel(Base, TypesMixin):
    __tablename__ = "users_customuser"

    username: Mapped[str_128] = mapped_column(unique=True)

    one_time_token: Mapped[Optional['OneTimeActivateTokenModel']] = relationship(
        uselist=False,
        back_populates='user'
    )


class OneTimeActivateTokenModel(Base, TypesMixin):
    __tablename__ = "users_onetimetoken"

    token: Mapped[str_32] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    expires_at: Mapped[datetime] = mapped_column(DateTime)

    user_id: Mapped[int] = mapped_column(ForeignKey("users_customuser.id", ondelete='CASCADE'))
    user: Mapped['UserModel'] = relationship(back_populates='one_time_token')
