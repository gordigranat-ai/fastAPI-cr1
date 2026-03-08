from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import re

# Модель для задания 1.4
class User(BaseModel):
    name: str
    id: int

# Модель для задания 1.5
class UserWithAge(BaseModel):
    name: str
    age: int

# Модель для задания 2.1 и 2.2
class Feedback(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Имя пользователя от 2 до 50 символов")
    message: str = Field(..., min_length=10, max_length=500, description="Сообщение отзыва от 10 до 500 символов")
    
    # Кастомная валидация для задания 2.2
    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        # Список недопустимых слов (в нижнем регистре для сравнения)
        forbidden_words = ['кринг', 'рофл', 'вайб']
        
        # Приводим сообщение к нижнему регистру для проверки
        message_lower = v.lower()
        
        # Проверяем каждое запрещенное слово
        for word in forbidden_words:
            # Используем регулярное выражение для поиска слова как целого слова
            pattern = r'\b' + re.escape(word) + r'\b'
            if re.search(pattern, message_lower):
                raise ValueError('Использование недопустимых слов')
        
        return v

# Хранилище данных (в реальном проекте использовалась бы БД)
# Для задания 2.1 и 2.2
feedbacks: List[Feedback] = []