from aiohttp import web

app = web.Application()
router = web.RouteTableDef()


@router.post('/image')
async def index(request):
    print(request)
    return web.Response(text="Hello, world")

app.add_routes(router)
web.run_app(app)
