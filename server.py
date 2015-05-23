#!/usr/bin/python
# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse, urllib, json, time
import analyzer
import pydoc #paged output
host_port = ('localhost', 8000)
iniciado = True
process = None
salida = []
s = -1
class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global iniciado, process, salida, s
        parsed_path = urlparse.urlparse(self.path)
        message = parsed_path.query
        message = message.strip()
        message = urllib.unquote(message).decode('utf8')
        q = message[0:2]
        if q=='q=':
            message = message[2:]
        message = message.replace('+',' ')
        #print message
        salidax = None
        if message=='quit':
            if iniciado == True:
                iniciado = False
                rc = analyzer.closeProcessConnection(process)
                if rc==0:
                    salidax = 'Analyzer detenido. Return code: '+str(rc)
                else:
                    salidax = 'No se pudo detener Analyzer. Return code: '+str(rc)
        elif message=='':
            message==""
            print u"  >> Mensaje vacío"
        else:
            if iniciado == True:
                print "  >> Analizar:",message
                process,salida,s = analyzer.sendLineToProcess([message.encode('utf-8')],process,[],-1)
                #salidax = salida[0]
                if len(salida)>1:
                    if len(salida[1])==1:
                        salidax = salida
                    else:
                        salidax = salida[0]
                else:
                    if len(salida[0])>1:
                        salidax = salida[0]
                    else:
                        salidax = salida[0][0]
                print "  >> Salida: ",salidax
                salidax = json.dumps( salidax )
                """
                salidax = []
                for sa in salida:
                    sal = []
                    for s in sa:
                        sal.append(" ".join(s))
                    sal = "<br>".join(sal)
                    salidax.append(sal)
                salidax = '<html><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><body>'+'<br><br>'.join(salidax)+'</body></html>'
                """
        self.send_response(200)
        if salidax is None:
            print "  >> None:", message
            salidax = '<html><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><body><form><input name="q" type="text" value="'+message+'" size="40"><input type="submit" value="OK"></form></body></html>'
            self.send_header('Content-Type', 'text/html')
        else:
            self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(salidax)
        return

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    print "------------------------------------------------------------------------------"
    print u"  >> Iniciando conexión con analyzer."
    print u"  >> Ingrese un comando de ejecución del tipo:"
    print u"  >>     analyzer.exe changapoeta -f analyzer.cfg"
    server = HTTPServer(host_port, GetHandler)
    do=True
    while do:
        print('-------------------------------------------')
        prog = raw_input("Comando analyzer:").strip();
        if prog=="":
            #comando default
            prog=None
            do = False
        elif prog.lower()=='?':
            #despliega la ayuda
            ayuda = open('command.help', 'r')
            ayudatext = ayuda.read()
            pydoc.pager(ayudatext)
        else:
            #explota el comando que intentara ejecutar
            prog = prog.split(" ")
            do=False

    try:
        process,salida,s = analyzer.connectToFreeling(None)
    except Exception, e:
        raise
    print('-------------------------------------------')
    print u'  >> Iniciando servidor en http://localhost:8000. Use <Ctrl-C> para detener.'
    print u'  >> Fecha de inicio:',time.strftime("%Y-%m-%d %H:%M:%S")
    print u'  >> Envíe la variable GET "q" con una frase que desee analizar.'
    print u'  >> Ejemplo:'
    print u'  >>     http://'+":".join([str(x) for x in host_port])+u'/?q=El perro está feliz.'
    print "------------------------------------------------------------------------------"
    server.serve_forever()