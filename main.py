import asyncio
from getpass import getpass

from dotenv import load_dotenv

from src.api import activate_vk_account, activate_tg_account
from src.core import Session
from src.exceptions import TokenExpiredException
from src.models import UserModel
from src.repo import UserRepository
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

            token = getpass('Одноразовый токен активации: ')

            one_time_token = user.one_time_token
            await check_token_lifetime(one_time_token)

            if one_time_token := user.one_time_token:
                if one_time_token.token == token:
                    print('Добро пожаловать,', user.username)
                else:
                    print('Неверный токен.')
                    return
            else:
                print('Отсутствует токен активации.')
                return

        platform = input('Выберите платформу: \n1) ВКонтакте\n2) Telegram\n')
        match platform:
            case '1':
                print('Вы выбрали ВКонтакте')
                await activate_vk_account(one_time_token)
            case '2':
                print('Вы выбрали Telegram')
                await activate_tg_account(one_time_token)
            case _:
                print('Неверный выбор платформы')
        print('Успешная активация аккаунта.')
    except TokenExpiredException as TE:
        print(TE)
    except Exception as e:
        print(f'Произошла ошибка вида {e.__class__.__name__} при обработке аккаунта', e, e.__context__)


if __name__ == "__main__":
    asyncio.run(main())
