import json
import datetime


class classEntradaLog:
    def __init__(self, permiso):
        curDT = datetime.datetime.now()
        self.doorNumber = permiso.doorNumber
        self.rfidData = permiso.rfidTag
        self.personID = permiso.personID
        self.personName = permiso.personName
        self.curDT = str(curDT)
        self.permission = permiso.permission

    def postSQLite(self, con):
        with con:
            if len(self.rfidData) == 12:
                c = con.cursor()
                queryString = "INSERT INTO seguridad_entrada(puerta_num, tarjeta_RFID, persona_SEQ, persona, fecha_hora, permiso) VALUES (?,?,?,?,?,?)"
                c.execute(queryString, (self.doorNumber, self.rfidData, self.personID, self.personName, self.curDT, self.permission))
                con.commit()
                print "successful SQLite insert"
            else:
                print "SQLite insert error"

    def postJSON(self):
        jsonLog = [{'SEQ': self.doorNumber, 'puerta_num': self.doorNumber, 'tarjeta_RFID': self.rfidData,
                    'persona_SEQ': self.personID, 'persona': self.personName, 'fecha_hora': self.curDT,
                    'permiso': self.permission}]
        data_string = json.dumps(jsonLog)
        print 'JSON:', data_string