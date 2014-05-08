import linecache
import datetime
import piLock.configuration as conf
import os
import sys


currentDateTime = datetime.datetime.now()


class classErrorLog:
    def __init__(self, sysError):
        self.eType, self.eObj, self.eTB = sysError
        f = self.eTB.tb_frame

        self.lineNumber = self.eTB.tb_lineno

        self.fileName = os.path.split(f.f_code.co_filename)[1]

        linecache.checkcache(self.fileName)

        self.errorType = self.eType.__name__

        self.errorMsg = self.eObj

        self.lineStr = linecache.getline(self.fileName, self.lineNumber, f.f_globals).strip()


    def insertDbError(self):
        try:
            db = conf.sqlite3.connect(conf.dbPath)
            with db:
                cur = db.cursor()
                query = "INSERT INTO %s VALUES(:SEQ, :fecha, :error, :msj, :archivo, :linea, :cont)"
                insert = {'SEQ':conf.SEQ, 'fecha':currentDateTime, 'error': self.errorType, 'msj':self.errorMsg, 'archivo':self.fileName, 'linea':self.lineNumber, 'cont':self.lineStr}
                cur.execute(query % conf.errorTable, insert)
        except:
            classErrorLog(sys.exc_info())
            print "ERROR inside of the Error Log class!"
