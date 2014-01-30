import json
import datetime
import piLock.configuration as conf
import classErrorLog as errorLog
import sys


class classEntradaLog:
    def __init__(self, permiso):
        curDT = datetime.datetime.now()
        self.doorNumber = permiso.doorNumber
        self.rfidData = permiso.rfidTag
        self.personID = permiso.personID
        self.personName = permiso.personName
        self.curDT = str(curDT)
        self.permission = permiso.permission

    def postSQLite(self):
        try:
            with conf.db:
                if len(self.rfidData) == 12:
                    cur = conf.db.cursor()
                    queryString = "INSERT INTO seguridad_entrada(puerta_num, tarjeta_RFID, persona_SEQ, persona, fecha_hora, permiso) VALUES (?,?,?,?,?,?)"
                    cur.execute(queryString, (self.doorNumber, self.rfidData, self.personID, self.personName, self.curDT, self.permission))
                    conf.db.commit()
                    print "successful SQLite insert"
                else:
                    print "SQLite insert error"
        except:
            errorLog.classErrorLog(sys.exc_info())

    def postJSON(self):
        jsonLog = [{'SEQ': self.doorNumber, 'puerta_num': self.doorNumber, 'tarjeta_RFID': self.rfidData,
                    'persona_SEQ': self.personID, 'persona': self.personName, 'fecha_hora': self.curDT,
                    'permiso': self.permission}]
        data_string = json.dumps(jsonLog)
        print 'JSON:', data_string