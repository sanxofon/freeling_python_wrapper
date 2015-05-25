# -*- coding: utf-8 -*-


from subprocess import Popen, PIPE
import pprint, time
pp = pprint.PrettyPrinter(indent=4)

# <codecell>

def connectToFreeling(prog=None,mode=None,out=False):
    if prog is None:
        #You should change ../analyzer.exe to whatever the path is to your freeling installation
        #--inpf [plain, token, splitted, morfo, tagged, sense,dep]
        modes = ['plain', 'token', 'splitted', 'morfo', 'tagged', 'sense', 'dep']
        if mode not in modes:
            mode = None
        if mode is None:
            prog = ['c:\\freeling31\\bin\\analyzer.exe', 'changapoeta', '-f', 'analyzer.cfg']
        else:
            prog = ['c:\\freeling31\\bin\\analyzer.exe', '-inpf', mode, 'changapoeta', '-f', 'analyzer.cfg']
        print "Default command:"," ".join(prog)
    if out:
        print("Iniciando conexión")
    # Run "cat", which is a simple Linux program that prints it's input.
    try:
    	process = Popen(prog, shell=True, stdin=PIPE, stdout=PIPE,stderr=PIPE,close_fds=False)
    except:
        print("Error iniciando conexión")
    	return False,False,False
    salida = []
    s = -1
    pp = pprint.PrettyPrinter(indent=4)
    if out:
        print('-------------------------------------------')
    return process,salida,s

# <codecell>

def sendLineToProcess(command,process,salida,s,out=False):
    for c in command:
        s+=1
        salida.append([])
        c = c.strip()
        process.stdin.write(c)
        if c[-1:]=='.':
        	removeLast = False
        	process.stdin.write('\r\n')
        else:
        	removeLast = True
        	process.stdin.write('.\r\n')
        if out:
            print(c.strip())
        while True:
            psout = process.stdout.readline()
            if psout=='\r\n':
                break
            psout =  psout.strip()
            #if psout=='. . Fp 1' and eliminarPunto:
            #	continue
            salida[s].append(psout.split(" "))
        if out:
            pp.pprint(salida[s])
        if removeLast:
        	del salida[s][-1]
    return process,salida,s

# <codecell>

def closeProcessConnection(process,out=False):
    #process.stdin.write('\x1a')
    #salida = process.stdout.read()
    process.stdin.close()
    if out:
        print('-------------------------------------------')
        print('Esperando a que termine analyzer')
    process.wait()
    if out:
        print('analyzer ha terminado. Return code: %d' % process.returncode)
    return process.returncode
"""
# test 1 (list & sleep)
print('-------------------------------------------')
print("Iniciando Test 1")
print('-------------------------------------------')
# Connect
process,salida,s = connectToFreeling(None,None,True)
if process==False:
	print "Error iniciando conexión"
else:
	# Send & recieve
	command = ['La perra come caca.','No estoy seguro de que los acentos funcionen, no sé.']
	for i in range(5):
		process,salida,s = sendLineToProcess(command,process,salida,s,True)
		print(i+1)
		time.sleep(1)

	# Close and print
	rc = closeProcessConnection(process,True)
	if rc==0:
		print("Salida:",s)
		pp.pprint(salida)
	else:
		print("Error cerrando la conexión. Return Code:",rc)

# test 2 (input)
print('-------------------------------------------')
print("Iniciando Test 2")
print("Escriba 'quit' para salir")
print('-------------------------------------------')
process,salida,s = connectToFreeling()
while True:
	command=[]
	frase = raw_input("Frase:").strip()
	if frase=='quit':
		break
	command.append(frase)
	process,salida,s = sendLineToProcess(command,process,[],-1)
	print (salida)
"""