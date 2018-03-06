import sqlalchemy as sa


metadata = sa.MetaData()


class Base:
    table = None

    def __init__(self, conn):
        self.conn = conn

    def __getitem__(self, item):
        return self.table.c[item]

    async def find_one(self, *args):
        stmt = sa.select([self.table]).where(sa.and_(*args))
        result = await self.conn.execute(stmt)
        return await result.fetchone()

    async def create(self, **kwargs):
        stmt = self.table.insert().values(**kwargs)
        await self.conn.execute(stmt)

    async def update(self, *args, **kwargs):
        stmt = self.table.update().values(**kwargs)
        if args:
            stmt = stmt.where(sa.and_(*args))
        await self.conn.execute(stmt)

    async def delete(self, *args):
        stmt = self.table.delete()
        if args:
            stmt = stmt.where(sa.and_(*args))
        await self.conn.execute(stmt)