import asyncio
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict

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
