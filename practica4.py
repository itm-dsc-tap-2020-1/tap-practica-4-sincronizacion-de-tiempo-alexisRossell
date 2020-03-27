import datetime
from time import ctime
import ntplib
from subprocess import call
import os
import time

servidor_de_tiempo = ('time-a-g.nist.gov', 'time-b-g.nist.gov', 
		'time-c-g.nist.gov', 'time-a-wwv.nist.gov', 
		'time-b-wwv.nist.gov', 'time-c-wwv.nist.gov')

print("Obteniendo la hora del servidor NTP...")
servidor_respuesta = None
for servidor in servidor_de_tiempo:
	try:
		t1 = datetime.datetime.now()
		cliente_ntp = ntplib.NTPClient()
		respuesta = cliente_ntp.request(servidor)
		t2 = datetime.datetime.now()
		servidor_respuesta = servidor
		break
	except Exception:
		print(f'No se obtuvo respuesta del servidor {servidor}')
		respuesta = None
	time.sleep(5)

if not respuesta:
	exit()

print(f'Fecha y hora de inicio de peticion = {t1}')
print (f"Fecha y hora de llegada de peticion = {t2}")

hora_actual = datetime.datetime.strptime(ctime(respuesta.tx_time), "%a %b %d %H:%M:%S %Y")
print("Respuesta de " + servidor_respuesta +  ": " + str(hora_actual) + "\n")

ajuste = (t2 - t1) / 2
print(f"Ajuste: {ajuste}")

fecha_hora =  datetime.datetime.strptime(ctime(respuesta.tx_time), "%a %b %d %H:%M:%S %Y") + ajuste

# {month}{day}{hour}{minute}{year}
fecha_hora = str(fecha_hora)
month = fecha_hora[5:7] 
day = fecha_hora[8:10]
hour = fecha_hora[11:13]
minute = fecha_hora[14:16]
year = fecha_hora[ :4]

newTime = month+day+hour+minute+year

os.system(f'date -u {newTime}')
