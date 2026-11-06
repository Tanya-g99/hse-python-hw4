from datetime import datetime, timezone
from enum import StrEnum
from pydantic import BaseModel, Field, field_validator

class ReasonType(StrEnum):
    NETWORK = "нет доступа к сети"
    PHONE = "не работает телефон"
    EMAIL = "не приходят письма"

class Problem(BaseModel):
    reason: ReasonType
    detection_time: datetime

    @field_validator("detection_time")
    @classmethod
    def validate_detection_time(cls, value: datetime) -> datetime:
        # Перевод текущего времени сервера и времени из запроса в UTC для поддержки таймзон
        value_utc = value.astimezone(timezone.utc)
        current_utc = datetime.now(timezone.utc)

        if value_utc > current_utc:
            raise ValueError("Дата и время обнаружения проблемы не может быть в будущем")
        
        return value
