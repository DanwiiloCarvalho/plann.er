from app.db.session import Session


async def get_db():
    async with Session() as session:
        yield session
