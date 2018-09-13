from aiohttp import web
import socketio, json, os
from cgi import parse_qs, escape
import json
import mysql.connector

DB_HOST = "sql52.main-hosting.eu"
DB_NAME = "u817691809_elimu"
DB_USER = os.environ['DB_USER_ELIMU']
DB_PASS = os.environ['DB_PASS_ELIMU']

mydb = mysql.connector.connect(
  host=DB_HOST,
  user=DB_USER,
  password=DB_PASS,
  database=DB_NAME
)
cursor = mydb.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS scratch_data_analytics (
	id MEDIUMINT PRIMARY KEY AUTO_INCREMENT,
	sid VARCHAR(255),
	nome VARCHAR(255),
	evento VARCHAR(255),
	vm MEDIUMTEXT,
	data_insercao TIMESTAMP DEFAULT NOW()
)""")
# mydb.commit()
cursor.close()

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
    print('Evento: ' + data['evento'])
    info = json.loads(data['projeto'])
    test = json.dumps(info['targets'][1]['blocks'])
    print("Bloco: " + test)
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        cursor = mydb.cursor(prepared=True)
        cursor.execute("INSERT INTO scratch_data_analytics (sid,nome,evento,vm) VALUES (%s,%s,%s,%s)",(sid,users[sid].nickname,data['evento'],data['projeto']))
        cursor.close()
    except Exception as detail:
        print(detail)

@sio.on('disconnect')
def disconnect(sid):
    users.pop(sid)
    print('disconnect ', sid)

async def index(request):
    raise web.HTTPFound(location="https://andersou.github.io/scratch-gui")
    
#app.router.add_static('/', 'F:/Projects/TCC/elimu_scratch_analyzer/scratch-gui/build')
app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app, port=os.environ.get('PORT',8080))