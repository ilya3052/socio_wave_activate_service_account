import asyncio
from getpass import getpass

from dotenv import load_dotenv

from src.api import activate_vk_account, activate_tg_account
from src.core import Session
from src.exceptions import TokenExpiredException
from src.models import UserModel, OneTimeActivateTokenModel, ServiceAccountModel
from src.repo import UserRepository, OneTimeActivateTokenRepository
from src.utils.token import check_token_lifetime

load_dotenv('src/core/cfg/.env')


async def main():
    try:
        username = input('Введите имя пользователя: ')
        with Session() as session:
            user_repo = UserRepository(session)
            user: UserModel = user_repo.get_by_username(username)
            if not user:
                print('Пользователь не найден.')
                return

            print('Добро пожаловать,', user.username)

            token = getpass('Одноразовый токен активации: ')

            token_repo = OneTimeActivateTokenRepository(session)
            token_instance: OneTimeActivateTokenModel = token_repo.get_by_token(token)
            if not token_instance:
                print('Токен активации не найден.')
                return
            await check_token_lifetime(token_instance)

            account: ServiceAccountModel = token_instance.account
            platform: str = account.platform.alias

        match platform:
            case 'VK':
                print('Вы выбрали ВКонтакте')
                await activate_vk_account(token_instance, account.id)
            case 'TG':
                print('Вы выбрали Telegram')
                await activate_tg_account(token_instance, account.id)
            case _:
                print('Неверный выбор платформы')
        print('Успешная активация аккаунта.')
    except TokenExpiredException as TE:
        print(TE)
    except Exception as e:
        print(f'Произошла ошибка вида {e.__class__.__name__} при обработке аккаунта', e, e.__context__)


if __name__ == "__main__":
    asyncio.run(main())
