aiohttp + ClickHouse 

To start and connect to the database, you need to create a files: 
1) apps/settings.py
2) apps/models/models.py or or model names as names, example ---> apps/models/clicks.py


Sample file settings.py:

1)
```sh
DATABASES = {
    'NAME': database name,
    'HOST': ip databas,
    'PORT': 9000
}
```
2)
```sh
from aiochorm.models import Model
from aiochorm.fields import *
from aiochorm.engines import MergeTree
```
