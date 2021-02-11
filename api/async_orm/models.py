import pytz
import copy
from infi.clickhouse_orm.engines import MergeTree

from six import iteritems, with_metaclass
from infi.clickhouse_orm.models import ModelBase, Model as _Model, BufferModel, MergeModel, DistributedModel

from async_orm.query import AsyncQuerySet


class Model(_Model):
    @classmethod
    def objects_in_async(cls, database):
        return AsyncQuerySet(cls, database)

    @classmethod
    def from_list_new(cls, line, field_names, timezone_in_use=pytz.utc, database=None, fake_model=None):
        field_info = zip(field_names, line)
        kwargs = {}
        copy_model = copy.deepcopy(fake_model)
        for name, value in field_info:
            field = getattr(cls, name) if not fake_model else getattr(copy_model, name)
            if fake_model:
                copy_model.__setattr__(name, field.to_python(value, timezone_in_use))
            else:
                kwargs[name] = field.to_python(value, timezone_in_use)
        if kwargs:
            obj = cls(**kwargs)
            if database:
                obj.set_database(database)
            return obj
        return copy_model

    @classmethod
    def from_list(cls, line, field_names, timezone_in_use=pytz.utc, database=None, fake_model=None):
        from six import next
        values = iter(line)
        kwargs = {}

        for name in field_names:
            field = getattr(cls, name) if not fake_model else getattr(fake_model, name)
            kwargs[name] = field.to_python(next(values), timezone_in_use)

        obj = cls(**kwargs)
        if database is not None:
            obj.set_database(database)
        return obj


class FakeModel(Model):

    engine = MergeTree('ts', ('ts',))

    def create_fake_field(self, fields):
        for name, db_type in fields:
           setattr(self, name, self.added_field_type(db_type))

    def added_field_type(self, db_type):
        import infi.clickhouse_orm.fields as orm_fields
        if db_type.startswith('Enum'):
            return orm_fields.BaseEnumField.create_ad_hoc_field(db_type)
        if db_type.startswith('DateTime('):
            return orm_fields.DateTimeField()
        if db_type.startswith('Array'):
            inner_field = self.added_field_type(db_type[6: -1])
            return orm_fields.ArrayField(inner_field)
        if db_type.startswith('FixedString'):
            length = int(db_type[12: -1])
            return orm_fields.FixedStringField(length)
        if db_type.startswith('Decimal'):
            precision, scale = [int(n.strip()) for n in db_type[8: -1].split(',')]
            return orm_fields.DecimalField(precision, scale)
        if db_type.startswith('Nullable'):
            inner_field = self.added_field_type(db_type[9: -1])
            return orm_fields.NullableField(inner_field)
        name = db_type + 'Field'
        if not hasattr(orm_fields, name):
            raise NotImplementedError('No field class for %s' % db_type)
        return getattr(orm_fields, name)()