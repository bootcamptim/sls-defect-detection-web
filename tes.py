from flask import Flask, render_template, request, redirect, stream_with_context, Response
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np
import os
import cv2
import glob

models = []

for filename in os.listdir('models'):
    filepath = os.path.join('models', filename)
    if os.path.isfile(filepath):
        models.append(filepath)

# Flask Server
app = Flask(__name__)

imdir = 'output'
model_dir = 'models'

@app.route('/')
def index():
    models = os.listdir(model_dir)
    return render_template('index.html', models=models)

@app.route('/video_feed')
def video_feed():
    model = request.args.get('model')
    print(model)

    def generate():
        while True:
            list_of_files = glob.glob(f'{imdir}/*')  # get all files in the directory
            if list_of_files:  # if there are files
                latest_files = sorted(list_of_files, key=os.path.getctime, reverse=True)  # get all files sorted by time
                for latest_file in latest_files:  # iterate over the files
                    img = cv2.imread(latest_file)  # try to read the image
                    if img is not None and np.any(img):  # if the image is readable and not empty
                        (flag, encodedImage) = cv2.imencode(".jpg", img)  # encode the image
                        if not flag:
                            continue
                        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                              bytearray(encodedImage) + b'\r\n')  # yield the image data
                        break
                
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, threaded=True)