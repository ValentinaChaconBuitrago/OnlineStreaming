#!/usr/bin/env python
# coding: utf-8

import socket
import cv2
import sys
from threading import Thread, Lock
import sys


#---------------------------------------------------------------------------------------------------------------
#----------------------------------------------- SERVIDOR UDP --------------------------------------------------
#---------------------------------------------------------------------------------------------------------------

#127.0.0.1
host = "127.0.0.1"

#20001
port = int(input('Ingrese el puerto en el que desea escuchar conexiones (e.g: 20001,20002,20003): '))

#Direccion donde estan guardados los archivos de video del servidor
# "/Users/Valentina/Desktop/OnlineStreaming/Web/videos/"
dir_video = "/Users/Valentina/Desktop/OnlineStreaming/Web/videos/"
nom_video = input('Ingrese el nombre del archivo de video que desea transmitir: ')
#Indica si se inicia o no la transmision
running = True

#---------------------------------------------------------------------------------------------------------------

if(len(sys.argv) != 2):
        print("Usage : {} interface".format(sys.argv[0]))
        print("e.g. {} eth0".format(sys.argv[0]))
        sys.exit(-1)

debug = True
jpeg_quality = 10

class VideoGrabber(Thread):
        """A threaded video grabber.
        Attributes:
        encode_params ():
        cap (str):
        attr2 (:obj:`int`, optional): Description of `attr2`.
        """
        def __init__(self, jpeg_quality):
                """Constructor.
                Args:
                jpeg_quality (:obj:`int`): Quality of JPEG encoding, in 0, 100.
                """
                Thread.__init__(self)
                self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
                self.cap = cv2.VideoCapture(dir_video + nom_video)
                self.running = True
                self.buffer = None
                self.lock = Lock()

        def stop(self):
                self.running = False

        def get_buffer(self):
                """Method to access the encoded buffer.
                Returns:
                np.ndarray: the compressed image if one has been acquired. None otherwise.
                """
                if self.buffer is not None:
                        self.lock.acquire()
                        cpy = self.buffer.copy()
                        self.lock.release()
                        return cpy

        def run(self):
                while self.running:
                        success, img = self.cap.read()
                        if not success:
                                continue

                        # JPEG compression
                        # Protected by a lock
                        # As the main thread may asks to access the buffer
                        self.lock.acquire()
                        result, self.buffer = cv2.imencode('.jpg', img, self.encode_param)
                        self.lock.release()


grabber = VideoGrabber(jpeg_quality)
grabber.start()
get_message = lambda: grabber.get_buffer()



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = (host, port)

print('starting up on %s port %s\n' % server_address)

sock.bind(server_address)

while(running):
        data, address = sock.recvfrom(4)
        data = data.decode('utf-8')
        if(data == "get"):
                buffer = get_message()
                if buffer is None:
                        continue
                if len(buffer) > 65507:
                        print("The message is too large to be sent within a single UDP datagram. We do not handle splitting the message in multiple datagrams")
                        sock.sendto("FAIL".encode('utf-8'),address)
                        continue
                # We sent back the buffer to the client
                sock.sendto(buffer.tobytes(), address)
        elif(data == "quit"):
                grabber.stop()
                running = False

print("Quitting..")
grabber.join()
sock.close()
