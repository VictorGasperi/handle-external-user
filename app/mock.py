from datetime import datetime, timezone
import secrets
from app.exchange_code import ExchangeCode


class DynoSimulated:

    dyno = [
        ExchangeCode(
            code = 'abc',
            uid = 'User2',
            expiresAt = int(datetime.now(timezone.utc).timestamp()) + 300,
            usedAt = None
        )
    ]