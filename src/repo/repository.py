from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from src.models import PlatformModel, ServiceAccountModel, ServiceAccountDataModel, UserModel, OneTimeActivateTokenModel
from .base import BaseRepository


class PlatformRepository(BaseRepository[PlatformModel]):
    def __init__(self, session):
        super().__init__(session, PlatformModel)


class ServiceAccountRepository(BaseRepository[ServiceAccountModel]):
    def __init__(self, session):
        super().__init__(session, ServiceAccountModel)

    def get_by_app_id(self, app_id):
        try:
            return self.session.scalars(
                select(self.model).options(joinedload(self.model.data)).filter_by(app_id=app_id)
            ).one_or_none()
        except NoResultFound:
            raise


class ServiceAccountDataRepository(BaseRepository[ServiceAccountDataModel]):
    def __init__(self, session):
        super().__init__(session, ServiceAccountDataModel)

    def get_by_phone_number(self, phone_number):
        try:
            return self.session.scalars(
                select(self.model).options(joinedload(self.model.serviceAccount)).filter_by(phone_number=phone_number)
            ).one_or_none()
        except NoResultFound:
            raise


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, session):
        super().__init__(session, UserModel)

    def get_by_username(self, username):
        try:
            return self.session.scalars(
                select(self.model).filter_by(username=username)
            ).one_or_none()
        except NoResultFound:
            raise


class OneTimeActivateTokenRepository(BaseRepository[OneTimeActivateTokenModel]):
    def __init__(self, session):
        super().__init__(session, OneTimeActivateTokenModel)

    def get_by_token(self, token):
        try:
            return self.session.scalars(
                select(self.model).options(joinedload(self.model.account)).filter_by(token=token)
            ).one_or_none()
        except NoResultFound:
            raise
