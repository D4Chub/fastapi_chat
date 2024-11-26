import asyncio
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict

from sqlalchemy.sql.functions import current_user
from websockets import connect

from chat.dao import MessagesDAO
from chat.schemas import MessageRead, MessageCreate
from users.dao import UsersDAO
from users.dependencies import get_current_user
from users.models import User


router = APIRouter(prefix='/chat', tags=['Chat'])
templates = Jinja2Templates(directory='templates')


# Страница чата
@router.get("/", response_class=HTMLResponse, summary="Chat Page")
async def get_chat_page(request: Request, user_data: User = Depends(get_current_user)):
    users_all = await UsersDAO.find_all()
    return templates.TemplateResponse(
        "chat.html",
        {"request": request, "user": user_data, 'users_all': users_all}
    )


@router.get("/messages/{user_id}", response_model=List[MessageRead])
async def get_messages(user_id: int, current_user: User = Depends(get_current_user)):
    return await MessagesDAO.get_messages_between_users(user_id1=user_id, user_id2=current_user.id) or []


@router.post("/messages", response_model=MessageCreate)
async def send_message(message: MessageCreate, current_user: User = Depends(get_current_user)):
    await MessagesDAO.add(
        sender_id=current_user.id,
        content=message.content,
        recipient_id=message.recipient_id
    )

    return {"recipient_id": message.recipient_id, "content": message.content, "status": "ok"}
