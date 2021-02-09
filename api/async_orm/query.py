from copy import copy

from infi.clickhouse_orm.fields import NullableField, Int32Field
from infi.clickhouse_orm.query import (Operator, SimpleOperator, InOperator, LikeOperator, IExactOperator,
                                       NotOperator, BetweenOperator, register_operator, FOV, Q, QuerySet,
                                       AggregateQuerySet)
from infi.clickhouse_orm.utils import comma_join


class AsyncQuerySet(QuerySet):
    async def execute(self):
        return await self._database.select(self.as_sql(), self._model_cls)

    async def count(self):
        if self._distinct or self._limits:
            sql = u'SELECT count() FROM (%s)' % self.as_sql()
            raw = await self._database.raw(sql)
            return int(raw[0][0])
        conditions = (self._where_q & self._prewhere_q).to_sql(self._model_cls)
        return await self._database.count(self._model_cls, conditions)

    async def aggregate(self, *args, **kwargs):
        return AsyncAggregateQuerySet(self, args, kwargs)


class AsyncAggregateQuerySet(AsyncQuerySet):

    def __init__(self, base_qs, grouping_fields, calculated_fields):
        super(AsyncAggregateQuerySet, self).__init__(base_qs._model_cls, base_qs._database)
        assert calculated_fields, 'No calculated fields specified for aggregation'
        self._fields = grouping_fields
        self._grouping_fields = grouping_fields
        self._calculated_fields = calculated_fields
        self._order_by = list(base_qs._order_by)
        self._where_q = base_qs._where_q
        self._prewhere_q = base_qs._prewhere_q
        self._limits = base_qs._limits
        self._distinct = base_qs._distinct

    async def group_by(self, *args):
        """
        This method lets you specify the grouping fields explicitly. The `args` must
        be names of grouping fields or calculated fields that this queryset was
        created with.
        """
        for name in args:
            assert name in self._fields or name in self._calculated_fields, \
                   'Cannot group by `%s` since it is not included in the query' % name
        qs = await copy(self)
        qs._grouping_fields = args
        return qs

    async def count(self):
        """
        Returns the number of rows after aggregation.
        """
        sql = u'SELECT count() FROM (%s)' % self.as_sql()
        raw = await self._database.raw(sql)
        return int(raw) if raw else 0

    async def execute(self):
        return await self._database.select(self.as_sql())

    def select_fields_as_sql(self):
        """
        Returns the selected fields or expressions as a SQL string.
        """
        return comma_join(list(self._fields) + ['%s AS %s' % (v, k) for k, v in self._calculated_fields.items()])