from typing import Optional 

from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from db.models import Users,UTMInfo,Notification
from db.session import async_session_maker


class UsersService:

    @staticmethod
    async def add_new_user(
            tg_id: int,
            tg_name: Optional[str],
            lang: str,
            utm: Optional[str] = None
            ) -> None:
        async with async_session_maker() as session:
            try:
                new_user = Users(
                    tg_id=tg_id,
                    tg_name=tg_name,
                    lang=lang,
                    utm=utm
                    )
                session.add(new_user)
                await session.commit()
            except IntegrityError:
                await session.rollback()


    @staticmethod
    async def check_exist_user(tg_id: int) -> bool:
        async with async_session_maker() as session:
            result = await session.execute(
                select(Users).where(Users.tg_id == tg_id)
            )
            return result.scalar_one_or_none() is not None
