from aiohttp import web
from apps.views import InfoClickView, clicks_count

def setup_routes(app):
    app.add_routes([
        web.view('/find_clicks/{company}/', InfoClickView),
        web.get('/count/', clicks_count)
    ])