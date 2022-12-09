from aiohttp.web_app import Application
from aiohttp.web_request import Request
from aiohttp.web_response import json_response
from aiohttp.web_routedef import RouteTableDef

router = RouteTableDef()


@router.get(path='/status/')
def status(request: Request):
    return json_response(data={'ok': True}, status=200)


def setup(*, web_app: Application):
    web_app.router.add_routes(router)
