import time
import RPIO
from classes.classPermiso import *
from classes.classEntradaLog import *
import classes.classErrorLog as errorLog
import configuration as conf
#from classes.classKeypad import *


########################################################################################################################
## Setup static variables


currentTime = time.strftime("%H:%M:%S", time.localtime())
currentDate = time.strftime("%Y-%m-%d", time.localtime())
currentDay = datetime.datetime.today().weekday()
currentDateTime = datetime.datetime.now()

errorCount = 0


########################################################################################################################
## Function to determine whether RFID tag scanned is valid for entry

def findTag(inputTag):
    permiso = classPermiso(inputTag)

    entry = classEntradaLog(permiso)
    entry.postSQLite(), entry.postJSON()

    if currentDay is 7: dateIsSunday = True
    else: dateIsSunday = False

    if permiso.permission == conf.PERMISSION_YES:
        if (permiso.endHour > currentTime > permiso.startHour) or (permiso.startHour is None and permiso.endHour is None):
            if currentDate < permiso.endDate:
                if ((dateIsSunday is True) and permiso.sundayPermission == 1) or (dateIsSunday is False):
                    entry = classEntradaLog(permiso)
                    entry.postSQLite(), entry.postJSON()
                    LED("green")
                    time.sleep(1)
                    return "Access Granted"
                else:
                    LED("red")
                    entry = classEntradaLog(permiso)
                    entry.postSQLite(), entry.postJSON()
                    time.sleep(1)
                    return "Cannot enter on a Sunday"
            else:
                LED("red")
                entry = classEntradaLog(permiso)
                entry.postSQLite(), entry.postJSON()
                time.sleep(1)
                return "Date is too old"
        else:
            LED("red")
            entry = classEntradaLog(permiso)
            entry.postSQLite(), entry.postJSON()
            time.sleep(1)
            return "You are not permitted to enter at this Time"

    elif permiso.permission == conf.PERMISSION_NO:
        entry = classEntradaLog(permiso)
        entry.postSQLite(), entry.postJSON()
        LED("red")
        time.sleep(1)
        return "Access Denied"

    elif permiso.permission == conf.PERMISSION_BLACKLIST:
        entry = classEntradaLog(permiso)
        entry.postSQLite(), entry.postJSON()
        LED("red")
        time.sleep(1)
        return "!!! Alert !!!"

    elif permiso.permission == conf.PERMISSION_PIN:
        if (permiso.endHour > currentTime > permiso.startHour) or (permiso.startHour is None and permiso.endHour is None):
            if currentDate < permiso.endDate:
                if ((dateIsSunday is True) and permiso.sundayPermission == 1) or (dateIsSunday is False):
                    entry = classEntradaLog(permiso)
                    entry.postSQLite(), entry.postJSON()
                    #pinInput(permiso.personPIN)
                else:
                    entry = classEntradaLog(permiso)
                    entry.postSQLite(), entry.postJSON()
                    return "Cannot enter on a Sunday"
            else:
                entry = classEntradaLog(permiso)
                entry.postSQLite(), entry.postJSON()
                return "Date is too old"
        else:
            entry = classEntradaLog(permiso)
            entry.postSQLite(), entry.postJSON()
            return "You are not permitted to enter at this Time"
    else:
        entry = classEntradaLog(permiso)
        entry.postSQLite(), entry.postJSON()
        return "Unkown Permission"


########################################################################################################################

conf.ser.open()

if conf.ser.isOpen():
    print "Open: " + conf.ser.portstr


def readCard():
    global errorCount
    try:
        LED("blue")
        while True:
            conf.ser.flushInput()
            LED("blue")
            rfidData = conf.ser.readline().strip()
            print "Line: "
            if len(rfidData) > 0:
                rfidData = rfidData[1:13]
                print "Card Scanned: ", rfidData
                print findTag(rfidData)

    except:
        errorLog.classErrorLog(sys.exc_info())

    finally:
        conf.ser.close()
        conf.db.close()
        RPIO.cleanup()


########################################################################################################################

def LED(colorON):
        if colorON == "green":
            RPIO.output(conf.GREEN, True)
            RPIO.output(conf.RED, False)
            RPIO.output(conf.BLUE, False)
            time.sleep(1)

        elif colorON == "red":
            RPIO.output(conf.GREEN, False)
            RPIO.output(conf.RED, True)
            RPIO.output(conf.BLUE, False)
            time.sleep(1)

        elif colorON == "blue":
            RPIO.output(conf.GREEN, False)
            RPIO.output(conf.RED, False)
            RPIO.output(conf.BLUE, True)

        else:
            return "Error"

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
