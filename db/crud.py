from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from db.models import Users
from db.session import async_session_maker

class UsersService:
    def __init__(self, async_session_maker):
        self.session_maker = async_session_maker

    async def add_new_user(self, tg_id: int, tg_name: Optional[str], lang: str, utm: Optional[str] = None) -> None:
        async with self.session_maker() as session:
            new_user = Users(tg_id=tg_id, tg_name=tg_name, lang=lang, utm=utm)
            session.add(new_user)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise


    async def check_exist_user(self, tg_id: int) -> bool:
        async with self.session_maker() as session:
            result = await session.execute(select(Users).where(Users.tg_id == tg_id))
            return result.scalar_one_or_none() is not None
