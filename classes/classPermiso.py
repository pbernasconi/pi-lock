import sys
import piLock.configuration as conf
import classErrorLog as errorLog


class classPermiso:
    def __init__(self, tag):
        self.rfidTag = tag
        try:
            with conf.db:
                c = conf.db.cursor()
                c.execute("SELECT * FROM %s WHERE (tarjeta_RFID=:x)" % conf.permisoTable, {"x": self.rfidTag})
                row = c.fetchone()

                if row is None:
                    self.tagRecognized = conf.NO
                    self.doorNumber = None
                    self.permission = conf.PERMISSION_NO
                    self.personID = None
                    self.personName = None
                    self.personPIN = None
                    self.personPhoto = None
                    self.startHour = "00:00:00"
                    self.endHour = "24:00:00"
                    self.sundayPermission = "0"
                    self.endDate = "2100-01-01"

                else:
                    self.tagRecognized = conf.YES
                    self.doorNumber = row[1]
                    self.personID = row[3]
                    self.personName = row[4]
                    self.personPIN = int(row[5])
                    self.permission = row[6]
                    self.sundayPermission = row[7]
                    self.startHour = row[8]
                    self.endHour = row[9]
                    self.endDate = row[10]

        except:
            errorLog.classErrorLog(sys.exc_info())