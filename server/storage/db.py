import asyncpg

from server import config


class DB:
    def __init__(self):
        self.pool = None

    async def start(self):
        self.pool = await asyncpg.create_pool(
            dsn=config.get_postgres_dsn(),
        )

    async def close(self):
        await self.pool.close()

    async def execute(self, sql, *args, conn=None, **kwargs):
        if conn:
            return await conn.execute(
                sql,
                *args,
                **kwargs
            )

        return await self.pool.execute(
            sql,
            *args,
            **kwargs
        )

    async def fetch(self, sql, *args, conn=None, **kwargs):
        if conn:
            result = await conn.fetch(sql, *args, **kwargs)
        else:
            result = await self.pool.fetch(sql, *args, **kwargs)

        return [
            dict(row)
            for row in result
        ]

    async def fetchrow(self, sql, *args, conn=None, **kwargs):
        if conn:
            result = await conn.fetchrow(sql, *args, **kwargs)
        else:
            result = await self.pool.fetchrow(sql, *args, **kwargs)

        return dict(result) if result else None


db = DB()
