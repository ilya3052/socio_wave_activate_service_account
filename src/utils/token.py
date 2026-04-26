from datetime import datetime, timezone

from src.core import Session
from src.exceptions import TokenExpiredException
from src.models import OneTimeActivateTokenModel


async def check_token_lifetime(token: OneTimeActivateTokenModel):
    if token.expires_at <= datetime.now(timezone.utc):
        with Session() as session:
            session.delete(token)
            session.commit()
        raise TokenExpiredException('Срок действия токена истек.')
