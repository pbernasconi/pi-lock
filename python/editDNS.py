# File which uses shell commands to:
#  edit IP, DNS, WIFI numbers
#  reboot RPI
#  install python libraries
#  create the stating script
import subprocess
from time import *
import sqlite3
import os

########################################################################################################################
DOOR_NUMBER = 101

NETWORK = "Airport"
PASSOWRD = "passpass"

IP_ADDRESS = "192.168.0.53"
SUB_MASK = "255.255.255.0"
ROUTER = "192.168.0.12"

DNS = "212.40.0.10"

########################################################################################################################
current_dir = os.path.dirname(os.path.abspath(__file__))
DBpath = os.path.join(current_dir, 'RFID_Lock.sqlite')

con = sqlite3.connect(DBpath)


########################################################################################################################
def readSqlite():
    with con:
        global personID, personName, personPIN, currentDate, currentTime, tagRecognized, dateIsSunday, doorNumber
        c = con.cursor()

        c.execute("SELECT * FROM seguridad_puerta")
        row = c.fetchone()

        ipNumber = row[5]
        dnsNumber = row[9]
        subnetNumber = row[10]
        routerNumber = row[11]
        wifiNetwork = row[12]
        wifiPassword = row[13]
        webPassword = row[14]


########################################################################################################################
def changeDNS(DNS):
    textDNS = "sudo echo 'nameserver %s' > '/etc/resolv.conf'" % (DNS)

    r = subprocess.Popen(textDNS, stdout=subprocess.PIPE, shell=True)

    for line in r.stdout.readlines():
        print line

    r.communicate()


########################################################################################################################
def changeIP():
    textIP = ["auto lo",
              "",
              "iface lo inet loopback",
              "iface etho inet dhcp",
              "",
              "allow-hotplug wlan0",
              "iface wlan0 inet static",
              "wpa-ssid %s" % NETWORK,
              "wpa-psk %s" % PASSOWRD,
              "address %s" % IP_ADDRESS,
              "netmask %s" % SUB_MASK,
              "network 192.168.0.0",
              "gateway %s" % ROUTER,
              "",
              "iface default inet dhcp"]

    joinedString = '\n'.join(textIP)
    print joinedString

    file = current_dir + "/interfaces"
    textFile = open(file, "w")
    textFile.write(joinedString)
    textFile.close()

    shellCall = "sudo mv %s/interfaces /etc/network" % (current_dir)

    r = subprocess.Popen(shellCall, stdout=subprocess.PIPE, shell=True)
    r.communicate()

    if r == "okay":
        subprocess.Popen("reboot", stdout=subprocess.PIPE, shell=True)


########################################################################################################################
def installLib():
    shellCalls = ["sudo apt-get update",
                  "sudo apt-get install python-setuptools",
                  "sudo apt-get install git-core",
                  "sudo apt-get install python-dev",
                  "sudo apt-get install python-pip",
                  "sudo easy_install -U pyserial",
                  "sudo easy_install -U RPIO",
                  "sudo easy_install -U cherrypy",
                  "sudo easy_install psutil"]

    testCall = ["sudo easy_install -U pyserial"]

    for i in range(len(testCall)):
        r = subprocess.Popen(testCall[i], stdout=subprocess.PIPE, shell=True)
        print testCall[i]

        for line in r.stdout.readlines():
            print line.strip()

        r.communicate()


########################################################################################################################
def installGitCode():
    textGit = ["cd ~",
               "git clone https://github.com/pbernasconi/piLock.git",
               "cd /piLock"]

    for i in range(len(textGit)):
        r = subprocess.Popen(textGit[i], stdout=subprocess.PIPE, shell=True)


########################################################################################################################
def createStartScript():
    textSS = ["### BEGIN INIT INFO",
              "# Provides: startScript",
              "# Required-Start: $remote_fs $syslog",
              "# Required-Stop: $remote_fs $syslog",
              "# Default-Start: 2 3 4 5",
              "# Default-Stop: 0 1 6",
              "# Short-Description: Simple script to start a program at boot",
              "# Description: A simple script from www.stuffaboutcode.com which will",
              "### END INIT INFO",
              "",
              "case '$1' in",
              "  start)",
              "    echo 'Starting Script'",
              "    python %s/readRFID" % current_dir,
              "    bash %s/modDNS.sh" % current_dir,
              "    python %s/systemStats.py" % current_dir,
              "    ;;",
              "  stop)",
              "    echo 'stopping Script'",
              "    killall python",
              "    ;;",
              "  *)",
              "    echo 'usage ...'",
              "    exit 1",
              "    ;;",
              "esac",
              "",
              "exit 0"]

    joinedString = '\n'.join(textSS)

    fileName = "startScript.sh"
    file = current_dir + "/" + fileName
    textFile = open(file, "w")
    textFile.write(joinedString)
    textFile.close()

    commands = ["sudo mv %s/%s /etc/init.d/" % (current_dir, fileName),
                "sudo chmod 755 /etc/init.d/%s" % (fileName),
                "sudo update-rc.d %s defaults" % (fileName)]

    for i in range(len(commands)):
        r = subprocess.Popen(commands[i], stdout=subprocess.PIPE, shell=True)
        print commands[i]


########################################################################################################################
def rebootPi():
    command = "sudo reboot"
    subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)


########################################################################################################################
if __name__ == '__main__':
    #readSqlite()
    #changeDNS(DNS)
    #changeIP()
    #installLib()
    #installGitCode()
    createStartScript()
