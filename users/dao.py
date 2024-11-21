from dao.base import BaseDao
from users.models import User


class UsersDAO(BaseDao):
    model = User
