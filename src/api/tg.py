from dotenv import load_dotenv
from telethon import TelegramClient

from src.core import Session
from src.core.config import API_ID, API_HASH, SESSION_FOLDER
from src.models import OneTimeActivateTokenModel, ServiceAccountModel, ServiceAccountDataModel
from src.repo import ServiceAccountDataRepository

load_dotenv('src/core/cfg/.env')


async def activate_in_platform(phone_number):
    session_path = f'{SESSION_FOLDER}/{phone_number}.session'
    client = TelegramClient(api_id=API_ID, api_hash=API_HASH, session=session_path)
    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(f'+{phone_number}')
            print(f"Код отправлен на номер телефона {phone_number}")
            code = input('Введите код: ')
            await client.sign_in(f'+{phone_number}', code)
    except Exception as e:
        print('Произошла ошибка при активации аккаунта на платформе', e)
        raise
    finally:
        client.disconnect()


async def activate_in_db(token: OneTimeActivateTokenModel, phone_number):
    try:
        session_path = f'{SESSION_FOLDER}/{phone_number}.session'
        with Session() as session:
            account_data_repo: ServiceAccountDataRepository = ServiceAccountDataRepository(session)

            account_data_instance: ServiceAccountDataModel = account_data_repo.get_by_phone_number(phone_number)

            account_instance: ServiceAccountModel = account_data_instance.serviceAccount
            account_instance.is_activated = True

            account_data_instance.session_path = session_path

            session.delete(token)
            session.commit()
    except Exception as e:
        print('Произошла ошибка при активации аккаунта в БД', e)
        raise


async def activate_tg_account(token: OneTimeActivateTokenModel):
    try:
        phone_number = input('Введите номер телефона (без + ): ')
        await activate_in_platform(phone_number)
        await activate_in_db(token, phone_number)
    except Exception as e:
        raise
