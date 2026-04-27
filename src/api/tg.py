from dotenv import load_dotenv
from telethon import TelegramClient

from src.core import Session
from src.core.config import API_ID, API_HASH, SESSION_FOLDER
from src.models import OneTimeActivateTokenModel, ServiceAccountModel, ServiceAccountDataModel
from src.repo import ServiceAccountRepository

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


async def activate_in_db(token: OneTimeActivateTokenModel, phone_number, account_id: int):
    try:
        session_path = f'{SESSION_FOLDER}/{phone_number}.session'
        with Session() as session:
            account_repo = ServiceAccountRepository(session)
            account: ServiceAccountModel = account_repo.get(account_id)

            account.is_activated = True
            account_data: ServiceAccountDataModel = account.data
            account_data.session_path = session_path

            session.delete(token)
            session.commit()
    except Exception as e:
        print('Произошла ошибка при активации аккаунта в БД', e)
        raise


async def activate_tg_account(token: OneTimeActivateTokenModel, account_id: int):
    try:
        phone_number = input('Введите номер телефона (без + ): ')
        await activate_in_platform(phone_number)
        await activate_in_db(token, phone_number, account_id)
    except Exception as e:
        raise
