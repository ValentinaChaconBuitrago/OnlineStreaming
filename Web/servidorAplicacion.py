from flask import Flask, render_template, request
from watson_developer_cloud import VisualRecognitionV3
import json
import cv2
import math
import os
import clienteUDP


#---------------------------------------------------------------------------------------------------------------
#--------------------------------------------- APLICACION FLASK ------------------------------------------------
#---------------------------------------------------------------------------------------------------------------

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__)


#Pagina principal
@app.route('/temp')
def home():
    return render_template("index.html")
#Pagina secundaria
@app.route('/procesar')
def about():
	clienteUDP
    return render_template("info.html")
#Pagina secundaria
@app.route('/')
def info():
    return render_template("index.html")

#Se llama aca cuando se sube el video, el cual lo guarda
@app.route("/procesar/",methods=["POST"])
def upload():
    #Todo este pedazo guarda la imagen
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    x= 0
    for file in request.files.getlist("file"):
        x+=1
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
        #Despues de guardar el video, lo que se hace es procesar el video, separandolo en mini imagenes y
        #Usando el api de watson
        carpetica = 'Uploads\\' + (filename[0:len(filename)-4] + str(x))
        print(carpetica)
        lim = procesar_video(dir = (path), video = filename, carpeta = 'Uploads/' + (filename[0:len(filename)-4] + str(x)))
        print("supuestamente proceso")
        num = contarJson(lim = lim, carpetica = carpetica)
    return render_template("info.html", numeroPersonas = num, nombreVideo = (filename[0:len(filename)-4]) + str(x))

if __name__ == '__main__':
    app.run(debug=True)