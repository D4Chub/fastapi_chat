from shutil import which

from dns.e164 import query
from sqlalchemy import select, and_, or_

from dao.base import BaseDao
from chat.models import Message
from database import async_session_maker


class MessagesDAO(BaseDao):
    model = Message

    @classmethod
    async def get_messages_between_users(cls, user_id1: int, user_id2: int):
        """
        Асинхронно возвращает все сообщения между пользователями

        Аргументы:
            user_id1: ID первого пользователя
            user_id2: ID второго пользователя

        Возвращает:
            Список сообщений между двумя пользователями
        """

        async with async_session_maker() as session:
            query = select(cls.model).filter(
                or_(
                    and_(cls.model.sender_id == user_id1, cls.model.recipient_id == user_id2),
                    and_(cls.model.sender_id == user_id2, cls.model.recipient_id == user_id1)
                )
            ).order_by(cls.model.id)
            result = await session.execute(query)
            return result.scalar().all()
