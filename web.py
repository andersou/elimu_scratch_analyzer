from aiohttp import web
import socketio
from cgi import parse_qs, escape


sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

users = dict()
class User:
    def __init__(self, sid, fingerprint):
        self.sid = sid
        self.fingerprint = fingerprint
        self.nickname = ""
    def setNickname(self, nickname):
        self.nickname = nickname
    def isLogado(self):
        return len(self.nickname) > 0
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return "{} : sid ({}), fingerprint ({})".format(self.nickname,self.sid,self.fingerprint)

@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    query_string = parse_qs(environ['QUERY_STRING'])
    users[sid] = User(sid, query_string['fingerprint'])


@sio.on('login')
async def login(sid, data):
    print("nome de usuario ", data)
    users[sid].setNickname(data)
    print(users)

@sio.on('dados_aluno')
async def dados_aluno(sid, data):
    print(data)


@sio.on('disconnect')
def disconnect(sid):
    users.pop(sid)
    print('disconnect ', sid)

app.router.add_static('/', './../scratch-gui/build')
# app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app)