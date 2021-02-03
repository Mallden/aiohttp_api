from aiohttp import web
from apps.views import info_clicks, clicks_count

def setup_routes(app):
    app.add_routes([
        web.get('/', info_clicks),
        web.get('/count/', clicks_count)
    ])