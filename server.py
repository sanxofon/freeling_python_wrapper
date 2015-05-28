#!/usr/bin/python
# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import urlparse, urllib, json, time
import analyzer
import pydoc #paged output
iniciado = True
process = None
salida = []
s = -1
cuantos = 0
##Parse arguments
import sys
stdout_encoding = sys.stdout.encoding

def getargs(argv):
    ihost=''
    iport = ''
    mode=None
    doit = False
    for i,arg in enumerate(argv):
        if arg == '-a':
            print u'python server.py -h <host> -p <port> -m <mode>'
            print u'Modes: tagged, plain, token, splitted, morfo, sense, dep'
            sys.exit()
        elif arg == "-x":
            doit = True
        else:
            try:
                narg = argv[i+1]
            except:
                break
                pass
            if arg == "-h":
                ihost = narg
            elif arg == "-p":
                iport = narg
            elif arg == "-m":
                mode = narg

    try:
        ihost = ishost.strip()
    except:
        ihost='localhost'
        pass
    #iport = raw_input("Port (8000):")
    try:
        iport = int(iport.strip())
    except:
        iport=8000
        pass
    modes = ['plain', 'token', 'splitted', 'morfo', 'tagged', 'sense', 'dep']
    if mode not in modes:
        mode=None
    return ihost,iport,mode,doit

class GetNPostHandler(BaseHTTPRequestHandler):
#class PostHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        global iniciado, process, salida, s, cuantos
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        # Begin the response
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        #self.wfile.write('Client: %s\n' % str(self.client_address))
        #self.wfile.write('User-agent: %s\n' % str(self.headers['user-agent']))
        #self.wfile.write('Path: %s\n' % self.path)
        #self.wfile.write('Form data:\n')

        # Echo back information about what was posted in the form
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # Se recibió un archivo de texto
                file_data = field_item.file.read()
                file_len = len(file_data)
                del file_data
                self.wfile.write('\tUploaded %s as "%s" (%d bytes)\n' % \
                        (field, field_item.filename, file_len))
            else:
                cadena = str(form[field].value).decode('utf-8').strip() #decode early
                if len(cadena)>0:
                    # Se recibió una cadena de texto
                    salida = []
                    s=-1
                    cuantos+=1
                    print " >> ",cuantos,":", cadena[0:50].encode(stdout_encoding)+"..." #encode late (print)
                    message = cadena.split(". ") #send decoded between python
                    #for m in messageu.split(". "):
                        #print m,salida,s,process
                    process,salida,s = analyzer.sendLineToProcess(message,process,salida,s)
                    salida = json.dumps( salida )
                    self.wfile.write(salida)
            break #sólo un campo field es aceptado
        return

#class GetHandler(BaseHTTPRequestHandler): 
    def do_GET(self):
        global iniciado, process, salida, s
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
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
                salida = []
                s=-1
                messageu = message.encode('utf-8').split(". ")
                #for m in messageu.split(". "):
                    #print m,salida,s,process
                process,salida,s = analyzer.sendLineToProcess(messageu,process,salida,s)
                """
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
                """
                salidax = salida
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
    ihost,iport,mode,doit = getargs(sys.argv[1:])
    from BaseHTTPServer import HTTPServer
    print "------------------------------------------------------------------------------"
    print "------------------------Freeling Analyzer Python Server-----------------------"
    #ihost = raw_input("Host (localhost):").strip()
    try:
        ihost=ihost.strip()
    except:
        ihost='localhost'
        pass
    #iport = raw_input("Port (8000):")
    try:
        iport = int(iport)
    except:
        iport=8000
        pass
    host_port = (ihost, iport)
    modes = ['plain', 'token', 'splitted', 'morfo', 'tagged', 'sense', 'dep']
    if mode not in modes:
        mode=None

    print u"  >> Iniciando conexión con analyzer en modo:",mode
    print u"  >> Ingrese un comando de ejecución del tipo:"
    print u"  >>     analyzer.exe changapoeta -f analyzer.cfg"

    server = HTTPServer(host_port, GetNPostHandler)
    do=True
    while do:
        print('-------------------------------------------')
        if doit:
            prog=""
        else:
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
        process,salida,s = analyzer.connectToFreeling(None,mode)
    except Exception, e:
        raise
    print('-------------------------------------------')
    print u'  >> Iniciando servidor en http://'+":".join([str(x) for x in host_port])+u'. Use <Ctrl-C> para detener.'
    print u'  >> Fecha de inicio:',time.strftime("%Y-%m-%d %H:%M:%S")
    print u'  >> Envíe la variable GET "q" con una frase que desee analizar.'
    print u'  >> Ejemplo:'
    print u'  >>     http://'+":".join([str(x) for x in host_port])+u'/?q=El perro está feliz.'
    print "------------------------------------------------------------------------------"
    server.serve_forever()