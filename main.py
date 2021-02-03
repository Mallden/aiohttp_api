import json

from aiohttp import web
from aiochorm import utils
from apps.models.models import ClickHouseCompanyLog
from apps.database import DB_CONNECT


async def handle(request):
    queryset = ClickHouseCompanyLog.objects_in_async(DB_CONNECT)

    if request.path == '/':
        queryset = queryset.filter(event=2)[:100]

    events = await queryset.execute()
    return web.json_response(text=json.dumps(events, cls=utils.JSONEncoder))


app = web.Application()
app.add_routes([
    web.get('/', handle),
])

web.run_app(app)
