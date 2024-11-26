from pydantic import BaseModel, Field


class MessageRead(BaseModel):
    id: int = Field(..., description="Уникальный ID сообщения")
    sender_id: int = Field(..., description="Уникальный ID отправителя")
    recipient_id: int = Field(..., description="Уникальный ID получателя")
    content: str = Field(..., description="Содержимое сообщения")


class MessageCreate(BaseModel):
    recipient_id: int = Field(..., description="Уникальный ID получателя")
    content: str = Field(..., description="Содержимое сообщения")
