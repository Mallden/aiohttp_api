from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web


class FirstTestCase(AioHTTPTestCase):

    async def get_application(self):
        from routes import setup_routes

        app = web.Application()
        setup_routes(app)
        return app


    @unittest_run_loop
    async def test_find_clicks(self):
        resp = await self.client.get("/find_clicks/44200/?start=2021.01.30&end=2021.01.31")
        assert resp.status == 200
        text = await resp.text()
        assert len(text) >= 1