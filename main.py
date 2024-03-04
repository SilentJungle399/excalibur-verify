from aiohttp import web

app = web.Application()
router = web.RouteTableDef()


@router.post('/image')
async def index(request):
    print(request)
    # recognize news from image
    return web.Response(text = "Hello, world")


@router.post('/text')
async def index(request):
    text = (await request.json())['text']
    print(text)

    return web.Response(text = "Hello, world")


app.add_routes(router)
web.run_app(app)
