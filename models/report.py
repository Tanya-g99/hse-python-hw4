import re

from datetime import date, datetime, time, timezone
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
from .problem import Problem

CYRILLIC_NAME_PATTERN = r"^[А-ЯЁ][а-яё]+$"
# Структура номера телефона:
# 1. префикс (+7 или 8)
# 2. код оператора (3 цифры в скобках или 3 цифры без скобок)
# 3. разделители (дефисы) между блоками цифр могут быть, но только в правильных местах
PHONE_PATTERN =  r"^(?:\+7|8)(?:\(\d{3}\)|\d{3})\d{3}(?:-\d{2}-\d{2}|\d{4})$"

class Report(BaseModel):
    last_name: str = Field(pattern=CYRILLIC_NAME_PATTERN)
    first_name: str = Field(pattern=CYRILLIC_NAME_PATTERN)
    birth_date: date
    phone: str = Field(pattern=PHONE_PATTERN)
    email: EmailStr

    problems: list[Problem] = Field(min_length=1)

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("Дата рождения должна быть меньше текущей даты")
        if value.year < 1900:
            raise ValueError("Некоррктная дата рождения")
        return value
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        # Приведение к единому стандарту с префиксом +7 и без скобок и дефисов
        cleaned = re.sub(r"[ \-()]", "", value)
        if cleaned.startswith("8"):
            cleaned = "+7" + cleaned[1:]
        
        return cleaned
    
    @model_validator(mode="after")
    def validate_report_dates(self) -> "Report":
        birth_datetime = datetime.combine(self.birth_date, time.min).replace(tzinfo=timezone.utc)
        
        for problem in self.problems:
            problem_utc = problem.detection_time.astimezone(timezone.utc)

            if problem_utc < birth_datetime:
                raise ValueError("Проблема не могла быть обнаружена раньше даты рождения абонента")
        return self
