from aiochorm.database import AsyncDatabase
from apps.settings import DATABASES

DB_CONNECT = AsyncDatabase(
    db_name=DATABASES['NAME'],
    db_host=DATABASES['HOST'],
    db_port=DATABASES['PORT'],
)
