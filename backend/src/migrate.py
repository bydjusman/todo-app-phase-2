#!/usr/bin/env python
"""Standalone database migration script."""

import sys
import asyncio

from config import settings
from models.database import Base, async_engine

async def run_migration():
    print('Connecting to database...')
    print(f'Database URL: {settings.database_url[:60]}...')
    try:
        async with async_engine.begin() as conn:
            print('Creating tables...')
            await conn.run_sync(Base.metadata.create_all)
        print('Migration completed successfully!')
    except Exception as e:
        print(f'Migration failed: {e}')
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(run_migration())
