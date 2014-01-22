import sqlite3 as lite
import os

PERMISSION_YES = 0
PERMISSION_NO = 1
YES = 1
NO = 0

current_dir = os.path.dirname(os.path.abspath(__file__))
DBpath = os.path.join(current_dir, '../RFID_Lock.sqlite')
con = lite.connect(DBpath)


class classPermiso:
    def __init__(self, tag):
        self.rfidTag = tag

        with con:
            c = con.cursor()
            c.execute("SELECT * FROM seguridad_permisos WHERE (tarjeta_RFID=:x)", {"x": self.rfidTag})
            pRow = c.fetchone()

            if pRow is None:
                self.tagRecognized = NO
                self.doorNumber = None
                self.permission = PERMISSION_NO
                self.personID = None
                self.personName = None
                self.personPIN = None
                self.personPhoto = None
                self.startHour = "00:00:00"
                self.endHour = "24:00:00"
                self.sundayPermission = "0"
                self.endDate = "2100-01-01"

            else:
                self.tagRecognized = YES
                self.doorNumber = pRow[1]
                self.personID = pRow[3]
                self.personName = pRow[4]
                self.personPIN = int(pRow[5])
                self.permission = pRow[6]
                self.sundayPermission = pRow[7]
                self.startHour = pRow[8]
                self.endHour = pRow[9]
                self.endDate = pRow[10]