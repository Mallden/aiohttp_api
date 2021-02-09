import datetime
import json

from aiohttp import web
from aiochorm import utils
from models import ClickHouseCompanyLog
from database import DB_CONNECT
from settings import DICT_KEY, TO_DATE

QUERYSET = ClickHouseCompanyLog.objects_in_async(DB_CONNECT)
FIELDS_MODEL = list(ClickHouseCompanyLog.fields().keys())

class InfoClickView(web.View):

    async def get(self):
        if not self.request.query:
            return web.json_response(status=400)

        data = dict(self.request.query)
        fields = data.pop('fields').split(',') if data.get('fields') else None

        filter_queryset = {
            DICT_KEY[key]
            if key in DICT_KEY.keys()
            else key: datetime.datetime.strptime(data[key], '%Y.%m.%d')
            if key in TO_DATE else data[key]
            for key in data
        }
        filter_queryset['company_id'] = int(self.request.match_info.get('company'))

        queryset = QUERYSET.filter(**filter_queryset).only(*fields) if fields else QUERYSET.filter(**filter_queryset)
        events = await queryset.execute()

        if not events:
            return web.json_response(status=204)

        return web.json_response(text=json.dumps(events, cls=utils.JSONEncoder))


async def clicks_count(request):
    if not request.query:
        return web.json_response({'error': 'Method Not Allowed', 'status code': 405})
    queryset = QUERYSET.filter(event=2).count()
    events = await queryset
    return web.json_response(text=json.dumps({'count': events}, cls=utils.JSONEncoder))
