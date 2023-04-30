from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np
import os
import cv2
import glob

# Flask Server
app = Flask(__name__)
socketio = SocketIO(app)

imdir = 'output'
model_dir = 'models'
loaded_models = {}

@app.route('/')
def index():
    models = os.listdir(model_dir)
    return render_template('index.html', models=models)

@app.route('/video_feed')
@app.route('/video_feed')
def video_feed():
    model_name = request.args.get('model')
    print(model_name)

    # Load the model if it has not been loaded yet
    if model_name not in loaded_models:
        model_path = os.path.join(model_dir, model_name)
        loaded_models[model_name] = tf.keras.models.load_model(model_path)

    model = loaded_models[model_name]

    def generate():
        while True:
            list_of_files = glob.glob(f'{imdir}/*')  # get all files in the directory
            if list_of_files:  # if there are files
                latest_files = sorted(list_of_files, key=os.path.getctime, reverse=True)  # get all files sorted by time
                for latest_file in latest_files:  # iterate over the files
                    img = cv2.imread(latest_file)  # try to read the image
                    if img is not None and np.any(img):  # if the image is readable and not empty
                        # Preprocess the image for the model
                        img_resized = cv2.resize(img, (640, 480))  
                        img_expanded = np.expand_dims(img_resized, axis=0)

                        # Make a prediction
                        prediction = model.predict(img_expanded)
                        result = "Defect" if prediction == 1 else "Ok" 
                        socketio.emit('prediction', {'data': result})  # send the prediction to the client                      

                        (flag, encodedImage) = cv2.imencode(".jpg", img)  # encode the image
                        if not flag:
                            continue
                        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                              bytearray(encodedImage) + b'\r\n')  # yield the image data
                        break
                
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5500)
