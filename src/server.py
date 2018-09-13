import socketio, json, os
from aiohttp import web
import src.database as db
from src.User import User
import src.db_pool as dbpool

users = dict()

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    users[sid] = User(sid)


@sio.on('login')
async def login(sid, data):
    print("nome de usuario ", sid, data)
    users[sid].setNickname(data)
    print(users)


@sio.on('dados_aluno')
async def dados_aluno(sid, data):
    aluno = users[sid]
    if not aluno.nickname:
        return
    dto = db.ScratchData(data['evento'],aluno,data['projeto'])
    dbpool.addRequisicao(dto)


@sio.on('disconnect')
def disconnect(sid):
    users.pop(sid)
    print('disconnect ', sid)


async def index(request):
    raise web.HTTPFound(location="https://andersou.github.io/scratch-gui")

async def teste(request):
    aluno = User("aaaaaaaa")
    aluno.setNickname("bbbb")
    dto = db.ScratchData("Teste", aluno, "vm")
    dbpool.addRequisicao(dto)
    return web.Response(text="Testou!")

app.router.add_get('/', index)
app.router.add_get('/teste', teste)
def run():
    db.init()
    dbpool.init()
    web.run_app(app, port=os.environ.get('PORT', 8081))

