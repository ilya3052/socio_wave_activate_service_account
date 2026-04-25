from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ParentSchemaConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='forbid', populate_by_name=True)


class PlatformSchema(ParentSchemaConfig):
    id: int = Field(
        alias="platform_id",
        description="Уникальный ID платформы"
    )
    name: str = Field(
        alias="platform_name",
        max_length=128,
        description="Название платформы"
    )


class ServiceAccountSchema(ParentSchemaConfig):
    id: int = Field(
        alias="serviceAccount_id",
        description="Уникальный ID сервисного аккаунта"
    )
    name: str = Field(
        alias="serviceAccount_name",
        max_length=128,
        description="Имя сервисного аккаунта на платформе"
    )

    app_id: Optional[int] = Field(
        alias="serviceAccountData_appId",
        description="ID приложения ВК",
        default=None
    )
    is_activated: bool = Field(
        alias="serviceAccount_isActivated",
        description="Статус активации сервисного аккаунта",
        default=False
    )

    platform_id: int = Field(description="Внешний ключ для связи с платформой")


class ServiceAccountDataSchema(ParentSchemaConfig):
    id: int = Field(
        alias="serviceAccountData_id",
        description="Уникальный ID записи о данных сервисного аккаунта"
    )
    service_key: Optional[str] = Field(
        alias="serviceAccountData_serviceKey",
        max_length=256,
        description="Сервисный ключ приложения ВК",
        default=None
    )
    protected_key: Optional[str] = Field(
        alias="serviceAccountData_protectedKey",
        max_length=256,
        description="Защищенный ключ приложения ВК",
        default=None
    )
    phone_number: Optional[str] = Field(
        alias="serviceAccountData_phoneNumber",
        min_length=11,
        max_length=11,
        description="Номер телефона аккаунта ТГ",
        pattern=r"^7\d{10}$",
        default=None
    )
    session_path: Optional[str] = Field(
        alias="serviceAccountData_sessionPath",
        max_length=256,
        description='Путь к файлу сессии аккаунта ТГ',
        default=None
    )

    serviceAccount_id: int = Field(description="Внешний ключ для связи с данными сервисного аккаунта")


class UserSchema(ParentSchemaConfig):
    id: int = Field(
        alias="user_id",
        description="Уникальный ID пользователя"
    )
    username: str = Field(
        alias="user_username",
        max_length=128,
        description="Имя пользователя"
    )


class OneTimeActivateTokenSchema(ParentSchemaConfig):
    id: int = Field(
        alias="oneTimeActivateToken_id",
        description="Уникальный ID токена"
    )
    token: str = Field(
        alias="oneTimeActivateToken_token",
        max_length=32,
        description="Одноразовый токен активации"
    )
    expires_at: str = Field(
        alias="oneTimeActivateToken_expiresAt",
        description="Время истечения токена"
    )

    user_id: int = Field(description="Внешний ключ для связи с пользователем")
