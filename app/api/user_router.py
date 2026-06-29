from typing import Annotated

from fastapi import Depends, Path, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User
from .deps import get_session
from .schemas import UpdateUser, UserBody, UserResponse

user_router = APIRouter(tags=["user"])


@user_router.post(
    "/user/",
    summary="Create user",
    description="This can only be done by the logged in user.",
)
async def create_user(
    body: UserBody, session: Annotated[AsyncSession, Depends(get_session)]
) -> JSONResponse:
    try:
        session.add(
            User(
                username=body.username,
                first_name=body.first_name,
                last_name=body.last_name,
                email=body.email,
                phone=body.phone,
            )
        )
        await session.commit()
    except SQLAlchemyError as error:
        logger.error(error)
        return JSONResponse({"message": "Failed operation"}, status_code=500)
    return JSONResponse({"message": "Successful operation"})


@user_router.get(
    "/user/{userId}",
    summary="Get user by id",
    description="Delete user with User ID supplied",
)
async def get_user_by_id(
    session: Annotated[AsyncSession, Depends(get_session)],
    user_id: int = Path(description="ID of user", ge=1, example=123, alias="userId"),
) -> UserResponse:
    """
    Returns a user based on a single ID.

    Если пользователь не имеет доступа к запрашиваемым данным, возвращается ошибка.

    - **userId**: Уникальный идентификатор пользователя
    """
    try:
        query = select(User).filter_by(id=user_id)
        result = await session.execute(query)
        user_info = result.scalar_one_or_none()

        if user_info:
            return UserResponse(
                username=user_info.username,
                first_name=user_info.first_name,
                last_name=user_info.last_name,
                email=user_info.email,
                phone=user_info.phone,
            )  # Преобразуем результат в объект модели
        else:
            raise ValueError(f"Пользователь с ID {user_id} не найден")
    except ValueError as error:
        return JSONResponse({"code": 0, "message": str(error)}, status_code=500)


@user_router.delete(
    "/user/{userId}",
    summary="Delete user by id",
    description="Delete user with User ID supplied",
)
async def delete_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    user_id: int = Path(description="ID of user", ge=1, example=123, alias="userId"),
) -> JSONResponse:
    try:
        query = select(User).filter_by(id=user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        await session.delete(user)
        await session.commit()
    except SQLAlchemyError as error:
        logger.error(error)
        return JSONResponse(
            content={"code": 0, "message": "Can't delete user"}, status_code=500
        )

    return Response(status_code=204)


@user_router.put(
    "/user/{userId}",
    summary="Delete user by id",
    description="Delete user with User ID supplied",
)
async def update_user(
    body: UpdateUser,
    session: Annotated[AsyncSession, Depends(get_session)],
    user_id: int = Path(description="ID of user", ge=1, example=123, alias="userId"),
) -> JSONResponse:
    try:
        query = select(User).filter_by(id=user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if user:
            user.first_name = body.first_name
            user.last_name = body.last_name
            user.email = body.email
            user.phone = body.phone
            await session.commit()
    except SQLAlchemyError as error:
        logger.error(error)
        return JSONResponse(
            content={"code": 0, "message": "Can't delete user"}, status_code=500
        )

    return JSONResponse({"message": "Successful operation"})
