import sqlite3 as lite
import time
import os
import datetime
import termios
import serial
from serial import SerialException
import RPIO
from classes.classPermiso import *
from classes.classSystemStats import *
from classes.classEntradaLog import *
from classes.classLED import *
#from classes.classKeypad import *


########################################################################################################################
## Setup static variables

PERMISSION_YES = 0
PERMISSION_NO = 1
PERMISSION_BLACKLIST = 2
PERMISSION_PIN = 3
YES = 1
NO = 0
sunday_permission = 1       #allowed
sunday_permission = 0       #not allowed

currentTime = time.strftime("%H:%M:%S", time.localtime())
currentDate = time.strftime("%Y-%m-%d", time.localtime())
currentDay = datetime.datetime.today().weekday()
currentDateTime = datetime.datetime.now()

errorCount = 0


current_dir = os.path.dirname(os.path.abspath(__file__))
DBpath = os.path.join(current_dir, 'RFID_Lock.sqlite')
con = lite.connect(DBpath)



########################################################################################################################
## Function to determine whether RFID tag scanned is valid for entry

def findTag(inputTag):

        permiso = classPermiso(inputTag)

        entry = classEntradaLog(permiso)
        entry.postSQLite(con), entry.postJSON()

        if currentDay is 7:
            dateIsSunday = True
        else:
            dateIsSunday = False


        if permiso.permission == PERMISSION_YES:
            if (permiso.endHour > currentTime > permiso.startHour) or (permiso.startHour is None and permiso.endHour is None):
                if currentDate < permiso.endDate:
                    if ((dateIsSunday is True) and permiso.sundayPermission == 1) or (dateIsSunday is False):
                        entry = classEntradaLog(permiso)
                        entry.postSQLite(con), entry.postJSON()
                        classLED("green")
                        time.sleep(1)
                        return "Access Granted"
                    else:
                        classLED("red")
                        time.sleep(1)
                        return "Cannot enter on a Sunday"
                else:
                    classLED("red")
                    time.sleep(1)
                    return "Date is too old"
            else:
                classLED("red")
                time.sleep(1)
                return "You are not permitted to enter at this Time"
    
        elif permiso.permission == PERMISSION_NO:
            entry = classEntradaLog(permiso)
            entry.postSQLite(con), entry.postJSON()
            classLED("red")
            time.sleep(1)
            return "Access Denied"

        elif permiso.permission == PERMISSION_BLACKLIST:
            entry = classEntradaLog(permiso)
            entry.postSQLite(con), entry.postJSON()
            classLED("red")
            time.sleep(1)
            mp3Location = current_dir + "/alarm.mp3"
            os.system('mpg321 ' + mp3Location + " &")
            return "!!! Alert !!!"

        elif permiso.permission == PERMISSION_PIN:
            if (permiso.endHour > currentTime > permiso.startHour) or (permiso.startHour is None and permiso.endHour is None):
                if currentDate < permiso.endDate:
                    if ((dateIsSunday is True) and permiso.sundayPermission == 1) or (dateIsSunday is False):
                        entry = classEntradaLog(permiso)
                        entry.postSQLite(con), entry.postJSON()
                        #pinInput(permiso.personPIN)
                    else:
                        return "Cannot enter on a Sunday"
                else:
                    return "Date is too old"
            else:
                return "You are not permitted to enter at this Time"
        else:
            return "Unkown Permission"


########################################################################################################################

rfidPort = "/dev/ttyAMA0"
ser = serial.Serial()
ser.baudrate = 9600
ser.port = rfidPort
ser.timeout = 0.1
ser.open()


if ser.isOpen():
    print "Open: " + ser.portstr


def readCard():
    global rfidData, errorCount
    try:
        classLED("blue")
        while True:
            ser.flushInput()
            classLED("blue")
            rfidData = ser.readline().strip()
            print "Line: "
            if len(rfidData) > 0:
                rfidData = rfidData[1:13]
                print "Card Scanned: ", rfidData
                print findTag(rfidData)

    except SerialException:
        print "Serial Exception error"
        errorCount+=1
        readCard()

    except termios.error:
        print "Termios error"
        errorCount+=1
        readCard()

    except OSError as e:
        if e.errno == 11:
            errorCount+=1
            readCard()
        else:
            raise

    finally:
        ser.close()
        con.close()
        RPIO.cleanup()
        pass
    
########################################################################################################################

'''
def pinInput(personPIN):

    #startTime = 60
    count = 0
    kp = keypad()

    print "Enter your PIN Code to proceed"

    def digit():
        r = None
        while r == None:
            r = kp.getKey()
        return r

    d1 = digit()
    time.sleep(0.5)

    d2 = digit()
    time.sleep(0.5)

    d3 = digit()
    time.sleep(0.5)

    d4 = digit()
    time.sleep(0.5)

    d5 = digit()

    pinEntry = d1, d2, d3, d4

    intPinEntry = int(''.join(map(str, pinEntry)))

    print "PIN ENTERED:", intPinEntry

    if d5 == "#":
        while personPIN != intPinEntry and (count < 4):
            time.sleep(1)
            count += 1
            endTime = datetime.datetime.now()
            if personPIN != pinEntry and (count == 4):
                classLED("red")
                print "Too many attempts, Access Denied"
                return
        else:
            classLED("green")
            time.sleep(2)
            print "PIN is correct, Access Granted"
    else:
        print "Do something here"

    #elapsedTime = (endTime - startTime)
    #print type(elapsedTime)

    #if elapsedTime > 60:
    #    return "PIN Entry Timed Out"

'''

###################################################################################################################

if __name__ == '__main__':
    readCard()

    print
    print "Number of errors incurred: ", errorCount
