import RPIO
import time

GREEN = 4
RED = 17
BLUE = 22


class classLED:
    def __init__(self, color):
        RPIO.setwarnings(False)
        RPIO.setup(GREEN, RPIO.OUT)
        RPIO.setup(RED, RPIO.OUT)
        RPIO.setup(BLUE, RPIO.OUT)
        self.colorIndicator(color)

    def colorIndicator(self, colorON):
        if colorON == "green":
            RPIO.output(GREEN, True)
            RPIO.output(RED, False)
            RPIO.output(BLUE, False)
            time.sleep(1)

        elif colorON == "red":
            RPIO.output(GREEN, False)
            RPIO.output(RED, True)
            RPIO.output(BLUE, False)
            time.sleep(1)

        elif colorON == "blue":
            RPIO.output(GREEN, False)
            RPIO.output(RED, False)
            RPIO.output(BLUE, True)

        else:
            return "Error"