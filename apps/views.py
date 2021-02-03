import datetime
import json

from aiohttp import web
from aiochorm import utils
from apps.models.models import ClickHouseCompanyLog
from apps.database import DB_CONNECT

QUERYSET = ClickHouseCompanyLog.objects_in_async(DB_CONNECT)

async def info_clicks(request):
    if not request.query:
        return web.json_response({'error': 'Method Not Allowed', 'status code': 405})
    print(dict(request.query))

    queryset = QUERYSET.filter(event=2, ts__gte=datetime.datetime.now() - datetime.timedelta(days=2))

    events = await queryset.execute()
    return web.json_response(text=json.dumps(events, cls=utils.JSONEncoder))

async def clicks_count(request):
    if not request.query:
        return web.json_response({'error': 'Method Not Allowed', 'status code': 405})
    queryset = QUERYSET.filter(event=2).count()
    events = await queryset
    return web.json_response(text=json.dumps({'count': events}, cls=utils.JSONEncoder))