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