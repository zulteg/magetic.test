import re

from aiohttp import web

from api import GamesAPI

routes = web.RouteTableDef()

api = GamesAPI(username='taras_kolomoets')


def search_filter(d: dict, search: str):
    if re.search(f'{search}', d.get('gamename'), re.I):
        return True
    if str(d.get('number')) == search:
        return True
    return False


@routes.get('/')
async def main(request):
    if not api.games_count:
        api.get_all_games(use_cache=True)
    data = api.games_json

    search = request.query.get('search')
    if search:
        data = [d for d in data if search_filter(d, search)]

    return web.json_response(data)


app = web.Application()
app.add_routes(routes)
web.run_app(app)
