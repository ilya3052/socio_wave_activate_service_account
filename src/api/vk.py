from getpass import getpass

from src.core import Session
from src.core.config import KEY
from src.models import OneTimeActivateTokenModel, ServiceAccountModel, ServiceAccountDataModel
from src.repo import ServiceAccountRepository
from src.utils.crypto import encrypt


async def activate_vk_account(token: OneTimeActivateTokenModel):
    try:
        with Session() as session:
            app_id = input('Введите app_id: ')

            account_repo = ServiceAccountRepository(session)
            account_instance: ServiceAccountModel = account_repo.get_by_app_id(app_id)

            account_instance.is_activated = True

            account_instance_data: ServiceAccountDataModel = account_instance.data

            service_key = getpass('Введите сервисный ключ: ')
            protected_key = getpass('Введите защищенный ключ: ')

            encrypted_service_key = encrypt(service_key, KEY)
            encrypted_protected_key = encrypt(protected_key, KEY)

            account_instance_data.service_key = encrypted_service_key
            account_instance_data.protected_key = encrypted_protected_key

            session.delete(token)
            session.commit()
    except Exception as e:
        print('Произошла ошибка при активации аккаунта', e)
        raise
