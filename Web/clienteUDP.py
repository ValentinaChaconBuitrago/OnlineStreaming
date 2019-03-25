#!/usr/bin/env python
# coding: utf-8

import socket
import cv2
import numpy as np
import sys
import time


#---------------------------------------------------------------------------------------------------------------
#----------------------------------------------- CLIENTE UDP --------------------------------------------------
#---------------------------------------------------------------------------------------------------------------


#Funcion con la que el cliente recibe la informacion del servidor de la aplicacion
def initiate():
    #Paramentros importantes para determinar el cliente a que puerto y direccion va a escuchar. De donde va a recibir la transmision de datos
	if(len(sys.argv) != 3):
	    print("Usage : {} hostname port".format(sys.argv[0]))
	    print("e.g.   {} 192.168.0.39 1080".format(sys.argv[0]))
	    sys.exit(-1)


	cv2.namedWindow("Image")

	#Creacion de un socket UDP
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Se guardan los datos entregados por el cliente
	host = sys.argv[1]
	port = int(sys.argv[2])
	server_address = (host, port)

	while(True):
	    sent = sock.sendto("get".encode('utf-8'), server_address)

	    data, server = sock.recvfrom(65507)
	    print("Fragment size : {}".format(len(data)))
	    if len(data) == 4:
	        # Mensaje de error que se envia al servidor
	        if(data == "FAIL"):
	            continue
	    array = np.frombuffer(data, dtype=np.dtype('uint8'))
	    img = cv2.imdecode(array, 1)
	    cv2.imshow("Image", img)
        #con la tecla q el cliente puede dejar de recibir la transmision del servidor
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        print("Asking the server to quit")
	        #sock.sendto("quit".encode('utf-8'), server_address)
	        print("Quitting")
	        break
initiate()
