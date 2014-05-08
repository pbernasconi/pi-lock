import cherrypy
import json
import sys
#import requests
from editDNS import *       # Including the editDNS.py file to use the rebootPi() and installGitCode() functions
#import configuration       conflict with DB variable name

current_dir = os.path.dirname(os.path.abspath(__file__))
DBpath = os.path.join(current_dir, 'RFID_Lock.sqlite')

class Root:
    @cherrypy.expose
    def index(self):
        """sends HTML when web user types:  http://localhost:8080/"""
        return """<html><head>
            <title>CherryPy RASPBERRY PI</title></head>
            <body>
            <a href="index.html">index.html</a>
            </body>
            </html>"""

    @cherrypy.expose
    def default(self, user):
        if user == 'JSON_texts':
            out = '[{"requiere_PIN":"0","IP_servidor":"192.168.100.1","zona":"fabrica","URL_servidor":"http://www.desa-net.com/TOTAI/db/","SEQ":"1","URL_puerta":"null","IP_puerta":"192168.100.2","puerta":"porton","time":"02:41:10"}]'
        elif user == 'stuff':
            out = "stuff goes back to the web browser"
        elif user == 'etc':
            out = "etc., etc."
        elif user == 'request':
            #r = requests.get('https://github.com/timeline.json')
            #out = r.text
            print
        else:
            out = "Unkown DEF request ! ! !"
        return out

    @cherrypy.expose
    def up(self, user):
        bodyJSON = cherrypy.request.body.read()
        print 'JSON: ' + bodyJSON
        JSONs = json.loads(bodyJSON)
        con = sqlite3.connect(DBpath)
        with con:
            cur = con.cursor()
            if user == 'putPermisos' or user == 'deletePermisos':
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
                    if user == 'putPermisos':
                        cur.execute("REPLACE INTO seguridad_permisos values(?,?,?,?,?,?,?,?,?,?,?)", all)
                    elif user == 'deletePermisos':
                        cur.execute("DELETE FROM seguridad_permisos WHERE tarjeta_RFID = %s" %i3)

                return "SUCESS: " +str(len(JSONs))+ " records"

            elif user == 'putPuerta':
                for item in JSONs:
                    i1 = item["SEQ"]
                    i2 = item["puerta"]
                    i3 = item["zona"]
                    i4 = item["requiere_PIN"]
                    i5 = item["alarma"]
                    i6 = item["IP_puerta"]
                    i7 = item["IP_servidor"]
                    i8 = item["URL_puerta"]
                    i9 = item["URL_servidor"]
                    i10 = item["DNS_puerta"]
                    i11 = item["Subnet_puerta"]
                    i12 = item["Router_puerta"]
                    i13 = item["WIFI_network"]
                    i14 = item["WIFI_contrasena"]
                    i15 = item["WEB_contrasena"]
                    all = [i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15]
                    cur.execute("REPLACE INTO seguridad_puerta values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", all)
                return "OK"

            elif user == 'RESTART_PI-LOCK':
                for item in JSONs:
                    if item["R_PI"] == "RESTART":
                        rebootPi()
                        cherrypy.engine.restart()
                    elif item["R_PI"] == "GitHub":
                        installGitCode()

            else: return "Unkown UP request !"


    @cherrypy.expose
    def db(self, user, page=None, limit=None):
        con = sqlite3.connect(DBpath)
        with con:
            cur = con.cursor()
            if user == 'getPuerta': cur.execute('select * from seguridad_puerta')
            elif user == 'getPermisos':
                if page == None: cur.execute('SELECT * FROM seguridad_permisos ORDER BY persona LIMIT 100 OFFSET 0')
                elif limit == None: cur.execute('SELECT * FROM seguridad_permisos ORDER BY persona LIMIT 10 OFFSET ?', (page))
                else:
                    pages = str(int(page)*int(limit))
                    cur.execute('SELECT * FROM seguridad_permisos ORDER BY persona LIMIT ? OFFSET ?', (limit, pages))
            elif user == 'getEntrada':
                if page == None: cur.execute('SELECT * FROM seguridad_entrada ORDER BY fecha_hora LIMIT 100 OFFSET 0')
                elif limit == None: cur.execute('SELECT * FROM seguridad_entrada ORDER BY fecha_hora LIMIT 10 OFFSET ?', (page))
                else:
                    pages = str(int(page)*int(limit))
                    cur.execute('SELECT * FROM seguridad_entrada ORDER BY fecha_hora LIMIT ? OFFSET ?', (limit, pages))
            elif user == 'getEntradaX': cur.execute('select * from seguridad_entrada limit 20')
            elif user == 'restart':
                cherrypy.engine.restart()
                raise cherrypy.HTTPRedirect("../", 307)
                python = sys.executable
                os.execl(python, python, * sys.argv)
                return "<html><body>Sorry, an error occured</body></html>"
            else: return "Unkown DB request !"
            # extract column names from selected table
            column_names = [d[0] for d in cur.description]
            reply = "["
            for row in cur:
                info = dict(zip(column_names, row))
                reply = reply + json.dumps(info) +","
            if user == 'getPuerta' :
                return reply[:-2] + '}]' #+ ',"time":"' + time.strftime('%d-%b %H:%M')
            else :
                return reply[:-1] + "]"

    @cherrypy.expose
    def writeIntoSQLite(self, newStatus=None, post=None):
        """Update the status file, inserting a timestamp and new status into a database"""
        con = sqlite3.connect(DBpath)
        stamp = time.time()
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Status(stamp INT, messages TEXT)")
            cur.execute("INSERT INTO Status VALUES(?, ?)", (stamp, newStatus))
            con.commit()
            print 'done !'
            return """<html>UPDATE YES !</html>"""


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cherrypy.config.update({'environment': 'production',
            'log.error_file': 'site.log',
            'log.screen': True})
    cherrypy.server.socket_host = '0.0.0.0'
    conf = {'/': {'tools.staticdir.on': True,
                'tools.staticdir.dir': os.path.join(current_dir, 'WebFiles'),
                'tools.staticdir.content_types': {'rss': 'application/xml',
                        'atom': 'application/atom+xml'}}}

    cherrypy.quickstart(Root(), '/', config=conf)