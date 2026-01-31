from typing import Optional
from pydantic import BaseModel


class ExchangeCode(BaseModel):
    code: str
    uid: str
    expiresAt: int
    usedAt: Optional[int]

    def to_dict(self):
        return {
            "code": self.code,
            "expiresAt": self.expiresAt
        }