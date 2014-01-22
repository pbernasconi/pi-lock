import RPIO
from time import sleep

class keypad():
    KEYPAD = [
    [1,2,3],
    [4,5,6],
    [7,8,9],
    ["*",0,"#"]
    ]
     
    ROW = [8, 10, 4, 25]
    COLUMN = [24, 23, 22]
     
    def __init__(self):
        RPIO.setmode(RPIO.BCM)
     
    def getKey(self):
        for j in range(len(self.COLUMN)):
            RPIO.setup(self.COLUMN[j], RPIO.OUT)
            RPIO.output(self.COLUMN[j], RPIO.LOW)
         
        for i in range(len(self.ROW)):
            RPIO.setup(self.ROW[i], RPIO.IN, pull_up_down=RPIO.PUD_UP)
         
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = RPIO.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i

        if rowVal < 0 or rowVal > 3:
            self.exit()
            return
         
        for j in range(len(self.COLUMN)):
                RPIO.setup(self.COLUMN[j], RPIO.IN, pull_up_down=RPIO.PUD_DOWN)
         
        RPIO.setup(self.ROW[rowVal], RPIO.OUT)
        RPIO.output(self.ROW[rowVal], RPIO.HIGH)

        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = RPIO.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j
                 
        if colVal < 0 or colVal > 2:
            self.exit()
            return
 
        self.exit()
        return self.KEYPAD[rowVal][colVal]
         
    def exit(self):
        for i in range(len(self.ROW)):
                RPIO.setup(self.ROW[i], RPIO.IN, pull_up_down=RPIO.PUD_UP) 
        for j in range(len(self.COLUMN)):
                RPIO.setup(self.COLUMN[j], RPIO.IN, pull_up_down=RPIO.PUD_UP)
         

kp = keypad()

def digit():
    r = None
    while r == None:
        r = kp.getKey()
    return r

print "Enter your PIN: "

finalEntry = ""
for i in range(0,4):
    pinEntry = str(digit())
    sleep(0.5)
    finalEntry = finalEntry + pinEntry

print finalEntry

d1 = str(digit())
print d1
sleep(0.5)
d2 = str(digit())
print d1 + d2
sleep(0.5)
d3 = str(digit())
print d1 + d2+ d3
sleep(0.5)
d4 = str(digit())
print d1 + d2+ d3 + d4















