from aiohttp import web
from views import InfoClickView, CountClickView


def setup_routes(app):
    app.add_routes([
        web.view('/find_clicks/{company}/', InfoClickView),
        web.get('/count/', CountClickView)
    ])