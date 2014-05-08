import os
import sqlite3
import serial
import classes.classErrorLog as errorLog
import sys


rootPath = os.path.dirname(os.path.abspath(__file__))
classesPath = os.path.join(rootPath, 'classes')
dbPath = os.path.join(rootPath, 'RFID_Lock.sqlite')

PERMISSION_YES = 0
PERMISSION_NO = 1
PERMISSION_BLACKLIST = 2
PERMISSION_PIN = 3
YES = 1
NO = 0

entradaTable = 'seguridad_entrada'
permisoTable = 'seguridad_permisos'
puertaTable = 'seguridad_puerta'
errorTable = 'registro_error'

doorNumber = 0
SEQ = 0

rfidPort = "/dev/ttyAMA0"
ser = serial.Serial()
ser.baudrate = 9600
ser.port = rfidPort
ser.timeout = 0.1


GREEN = 4
RED = 17
BLUE = 22

RPIO.setwarnings(False)
RPIO.setup(GREEN, RPIO.OUT)
RPIO.setup(RED, RPIO.OUT)
RPIO.setup(BLUE, RPIO.OUT)


try:
    db = sqlite3.connect(dbPath)
    with db:
        cur = db.cursor()
        cur.execute('SELECT codigo_puerta FROM %s' % puertaTable)
        doorNumber = cur.fetchone()
        cur.execute('SELECT SEQ FROM %s' % puertaTable)
        SEQ = cur.fetchone()

except:
    errorLog.classErrorLog(sys.exc_info())



print rootPath
print classesPath
print dbPath
print doorNumber[0]
print SEQ[0]