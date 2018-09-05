from aiohttp import web
import socketio, json
from cgi import parse_qs, escape


sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

users = dict()
class User:
    def __init__(self, sid):
        self.sid = sid
        self.nickname = ""
    def setNickname(self, nickname):
        self.nickname = nickname
    def isLogado(self):
        return len(self.nickname) > 0
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return "{} : sid ({})".format(self.nickname,self.sid)

@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    users[sid] = User(sid)
 

@sio.on('login')
async def login(sid, data):
    print("nome de usuario ",sid, data)
    users[sid].setNickname(data)
    print(users)

@sio.on('dados_aluno')
async def dados_aluno(sid, data):
    print("Usuario: ",users[sid])
    data = data[1:-1].replace("\\\"","\"")
    #data_json = json.loads(data[1:-1])
    print(json.dumps(json.loads(data), indent=4, sort_keys=True))
    print('oi')

@sio.on('disconnect')
def disconnect(sid):
    users.pop(sid)
    print('disconnect ', sid)

app.router.add_static('/', './../scratch-gui/build')
# app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app)