
import mysql.connector, os

DB_HOST = "sql52.main-hosting.eu"
DB_NAME = "u817691809_elimu"
DB_USER = os.environ['DB_USER_ELIMU']
DB_PASS = os.environ['DB_PASS_ELIMU']

def getConnection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

def init():
    mydb = getConnection()
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
    mydb.commit()
    cursor.close()

from datetime import datetime
class ScratchData:
    def __init__(self,evento, user,vm):
        self.evento = evento
        self.user = user
        self.vm = vm
        self.data_insercao = datetime.now()

    def getInsertParams(self):
        user = self.user
        return (user.sid,self.nome,self.evento,self.vm,self.data_insercao)

    @staticmethod
    def getInsertQuery():
        return "INSERT INTO scratch_data_analytics (sid,nome,evento,vm,data_insercao) VALUES (%s,%s,%s,%s,%s)"