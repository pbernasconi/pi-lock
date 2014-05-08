import urllib2
import json
import sqlite3
import os
from classes.classErrorLog import classErrorLog
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
DBpath = os.path.join(current_dir, 'RFID_Lock.sqlite')


def updateSQLite():
    try:
        jsonRequest = urllib2.urlopen("http://www.desa-net.com/TOTAI/dbm/seguridad_permios/").read()
        JSONs = json.loads(jsonRequest)
        db = sqlite3.connect(DBpath)
        with db:
            cur = db.cursor()
            print "DB was modified 1"
            #cur.execute("DELETE FROM seguridad_permisos")
            for item in JSONs:
                i1 = item["SEQ"]
                i2 = item["puerta_SEQ"]
                i3 = item["tarjeta_RFID"]
                i4 = item["persona_SEQ"]
                i5 = item["persona"]
                i6 = item["persona_PIN"]
                i7 = item["permiso"]
                i8 = item["domingo"]
                i9 = item["noche_inicio"]
                i10 = item["noche_fin"]
                i11 = item["fecha_vencida"]
                all = [i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11]
                print "DB was modified"
                if i2 == '002':
                    cur.execute("INSERT INTO seguridad_permisos values(?,?,?,?,?,?,?,?,?,?,?)", all)

            print "SUCESS: " + str(len(JSONs)) + " records"

    except Exception:
        classErrorLog(sys.exc_info())


updateSQLite()