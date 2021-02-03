from aiochorm.models import Model
from aiochorm.fields import *
from aiochorm.engines import MergeTree


class ClickHouseCompanyLog(Model):
    pg_id = NullableField(inner_field=Int32Field())
    company_id = NullableField(inner_field=Int32Field())
    event = NullableField(inner_field=Int8Field())
    referer_url = NullableField(inner_field=StringField())
    referer_url_name = NullableField(inner_field=StringField())
    section_id = NullableField(inner_field=Int32Field())
    ts = DateTimeField()
    ip = NullableField(inner_field=StringField())
    user_agent = NullableField(inner_field=StringField())
    url = NullableField(inner_field=StringField())
    showcase_id = NullableField(inner_field=Int32Field())
    advert_id = NullableField(inner_field=Int32Field())
    product_id = NullableField(inner_field=Int32Field())
    interior_id = NullableField(inner_field=Int32Field())
    profile_id = NullableField(inner_field=Int32Field())
    user_id = NullableField(inner_field=Int32Field())
    region_id = NullableField(inner_field=Int32Field())
    click_point = NullableField(inner_field=StringField())
    point_type = NullableField(inner_field=Int32Field())
    point_position = NullableField(inner_field=Int32Field())
    click_place = NullableField(inner_field=StringField())
    session = NullableField(inner_field=StringField())
    engine = MergeTree('ts', ('ts',))
