from http.client import responses
from os import access
from pyexpat.errors import messages
from tabnanny import check

from fastapi import APIRouter, Response
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from sqlalchemy.testing.suite.test_reflection import users

from exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException, PasswordMismatchException
from users.auth import get_password_hash, authenticate_user, create_access_token
from users.dao import UsersDAO
from users.schemas import SUserAuth, SUserRegister


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register/")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_more(email=user_data.email)
    if user:
        raise UserAlreadyExistsException

    if user_data.password != user_data.password_check:
        raise PasswordMismatchException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password
    )

    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/login/")
async def login_user(response: Response, user_data: SUserAuth) -> dict:
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key='user_access_token', value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token, 'refresh_token': None, 'message': 'Авторизация успешна!'}


@router.post("/logout/")
async def logout_user(response: Response) -> dict:
    response.delete_cookie(key="user_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}
