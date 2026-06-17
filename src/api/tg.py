import os
from typing import Any

from dotenv import load_dotenv
from telethon import TelegramClient
from getpass import getpass

from src.core import Session
from src.core.config import API_ID, API_HASH, SESSION_FOLDER
from src.models import OneTimeActivateTokenModel, ServiceAccountModel, ServiceAccountDataModel
from src.repo import ServiceAccountRepository

load_dotenv('src/core/cfg/.env')


def unique_path(path: str) -> tuple[str, int]:
    if not os.path.isfile(path):
        return path, 0
    root, ext = os.path.splitext(path)
    counter = 1
    while True:
        candidate = f'{root}-{counter}{ext}'
        if not os.path.isfile(candidate):
            return candidate, counter
        counter += 1


async def activate_in_platform(phone_number):
    session_path, attempt = unique_path(f'{SESSION_FOLDER}\\{phone_number}.session')
    client = TelegramClient(api_id=API_ID, api_hash=API_HASH, session=session_path, lang_code="ru", system_lang_code="ru-RU" )
    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(f'+{phone_number}')
            print(f"Код отправлен на номер телефона {phone_number}")
            code = getpass('Введите код: ')
            await client.sign_in(f'+{phone_number}', code)
            return attempt
    except Exception as e:
        print('Произошла ошибка при активации аккаунта на платформе', e)
        raise
    finally:
        await client.disconnect()


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

async def delete_session_duplicate_from_db(token, account_id):
    try:
        with Session() as session:
            account_repo = ServiceAccountRepository(session)
            account: ServiceAccountModel = account_repo.get(account_id)
            data = account.data

            session.delete(data)
            session.delete(account)
            session.delete(token)
            session.commit()
    except Exception as e:
        print('Произошла ошибка при активации аккаунта в БД', e)
        raise

async def activate_tg_account(token: OneTimeActivateTokenModel, account_id: int):
    try:
        with Session() as session:
            account_repo = ServiceAccountRepository(session)
            account: ServiceAccountModel = account_repo.get(account_id)
            phone_number = account.data.phone_number

        attempt = await activate_in_platform(phone_number)
        if attempt == 0:
            await activate_in_db(token, phone_number, account_id)
        else:
            await delete_session_duplicate_from_db(token, account_id)
    except Exception as e:
        raise
