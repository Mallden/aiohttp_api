import datetime
import json

from aiohttp import web
from aiochorm import utils
from models import ClickHouseCompanyLog
from database import DB_CONNECT
from settings import DICT_KEY, TO_DATE

QUERYSET = ClickHouseCompanyLog.objects_in_async(DB_CONNECT)
FIELDS_MODEL = list(ClickHouseCompanyLog.fields().keys())

def get_filter_info(data, fields_search=False):
    print(data)
    fields = data.pop('fields').split(',') if data.get('fields') else None
    filter_queryset = {
        DICT_KEY[key]
        if key in DICT_KEY.keys()
        else key: datetime.datetime.strptime(data[key], '%Y.%m.%d')
        if key in TO_DATE else data[key] if not '__in' in DICT_KEY.get(key) else data[key].split(',')
        for key in data
    }
    if fields_search:
        return fields, filter_queryset
    return filter_queryset


class InfoClickView(web.View):

    async def get(self):
        if not self.request.query:
            return web.json_response(status=400)

        data = dict(self.request.query)
        fields, filter_queryset = get_filter_info(data, fields=True)
        filter_queryset['company_id'] = int(self.request.match_info.get('company'))

        queryset = QUERYSET.filter(**filter_queryset).only(*fields) if fields else QUERYSET.filter(**filter_queryset)
        events = await queryset.execute()

        if not events:
            return web.json_response(status=204)

        list_events = list()
        for event in events:
            list_events.append(event.to_dict())
        return web.json_response(text=json.dumps(list_events, cls=utils.JSONEncoder))


class CountClickView(web.View):

    async def get(self):
        data = dict(self.request.query)
        filter_queryset = get_filter_info(data)
        print(filter_queryset)
        queryset = QUERYSET.filter(**filter_queryset).aggregate('company_id', count='count()')
        events = await self.get_events(queryset)
        events = events.group_by('company_id')
        events = await self.get_events(events)
        events = await events.execute()
        print(events)
        list_events = list()
        for event in events:
            list_events.append(event.__dict__)
        print(list_events)
        return web.json_response(text=json.dumps(list_events, cls=utils.JSONEncoder))

    @staticmethod
    def get_events(queryset):
        return queryset


