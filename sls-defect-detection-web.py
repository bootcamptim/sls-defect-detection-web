from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np
import os
import cv2
import glob
import queue
import threading
import time

# Flask Server
app = Flask(__name__)
socketio = SocketIO(app)

imdir = 'output'
model_dir = 'models'
loaded_models = {}
img_queue = queue.Queue(maxsize=10)

def image_queue_worker():
    while True:
        list_of_files = glob.glob(f'{imdir}/*')
        if list_of_files:
            latest_files = sorted(list_of_files, key=os.path.getctime, reverse=True)
            for latest_file in latest_files:
                file_size = os.path.getsize(latest_file)
                if file_size > 50000:  # Adjust the threshold as needed
                    img = cv2.imread(latest_file)
                    if img is not None and np.any(img):
                        try:
                            img_queue.put(img, block=False)
                        except queue.Full:
                            pass
                        break
        # time.sleep(0.05)

@app.route('/')
def index():
    models = os.listdir(model_dir)
    return render_template('index.html', models=models)

@app.route('/video_feed')
def video_feed():
    model_name = request.args.get('model')
    print(model_name)

    if model_name not in loaded_models:
        model_path = os.path.join(model_dir, model_name)
        loaded_models[model_name] = tf.keras.models.load_model(model_path)

    model = loaded_models[model_name]

    def generate():
        while True:
            try:
                img = img_queue.get(block=True, timeout=1)
                img_resized = cv2.resize(img, (640, 480))
                img_expanded = np.expand_dims(img_resized, axis=0)
                prediction = model.predict(img_expanded)
                result = "Defect" if prediction == 1 else "Ok"
                socketio.emit('prediction', {'data': result})

                (flag, encodedImage) = cv2.imencode(".jpg", img)
                if not flag:
                    continue
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                       bytearray(encodedImage) + b'\r\n')
            except queue.Empty:
                pass

    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    img_queue_worker_thread = threading.Thread(target=image_queue_worker)
    img_queue_worker_thread.start()
    socketio.run(app, host='0.0.0.0', port=5500)
