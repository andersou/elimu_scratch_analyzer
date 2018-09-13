import queue, asyncio, threading
import src.database as db
fila_req = queue.Queue()
async def processaRequisicao():
    while True:
        req = fila_req.get()
        print("Nova requisicao")
        print(req)
        db.getConnection()
        cursor = db.cursor()
        cursor.execute(db.ScratchData.getInsertQuery(),req.getInsertParams())

def init():
    loop = asyncio.new_event_loop()
    asyncio.async(processaRequisicao(),loop=loop)
    threading.Thread(target=loop.run_forever).start()

def addRequisicao(req):
    fila_req.put(req)