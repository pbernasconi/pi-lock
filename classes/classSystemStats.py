import psutil as p
import os
import json
from firebasin import Firebase
import piLock.configuration as conf

FIREBASE_URL = 'https://pilock.firebaseio.com'
fb = Firebase(FIREBASE_URL)

DOORNUMBER = 'door5'


class classSystemStats:
    def __init__(self):
        temp = os.popen('vcgencmd measure_temp').readline()
        self.cpuTemp = float(temp.replace("temp=", "").replace("'C\n", ""))
        self.totalRAM = self.b2k(p.virtual_memory().total)
        self.usedRAM = self.b2k(p.virtual_memory().used)
        self.availableRAM = self.b2k(p.virtual_memory().available)
        self.totalDiskSpace = self.b2k(p.disk_usage('/').total)
        self.usedDiskSpace = self.b2k(p.disk_usage('/').used)
        self.freeDiskSpace = self.b2k(p.disk_usage('/').free)
        self.cpuUsage = p.cpu_percent(interval=1)
        self.createJSON()

    def b2k(self, bts):
        kilobytes = bts / 1024
        return kilobytes

    def createJSON(self):
        jsonRawString = {
            'Total_RAM_(Kb)': self.totalRAM,
            'Used_RAM_(Kb)': self.usedRAM,
            'Available_RAM_(Kb)': self.availableRAM,
            'Total_Disk_Space_(Kb)': self.totalDiskSpace,
            'Used_Disk_Space_(Kb)': self.usedDiskSpace,
            'Free_Disk_Space_(Kb)': self.freeDiskSpace,
            'CPU_Usage_(%)': self.cpuUsage,
            'CPU_Temperature_(*C)': self.cpuTemp
        }
        data_string = json.dumps(jsonRawString)
        self.JSONstr = data_string

    def toString(self):
        print self.JSONstr

    def handleFirebase(self):
        #fb.child(DOORNUMBER).set(createJSON())
        fb.close()