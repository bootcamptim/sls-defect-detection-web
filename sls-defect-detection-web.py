from flask import Flask, render_template, request, redirect, url_for
import tensorflow as tf
import numpy as np
import os

# Flask Server
app = Flask(__name__)

@app.route('/', methods=['GET'])
def model_select():

    models = []
    for filename in os.listdir('models'):
        filepath = os.path.join('models', filename)
        if os.path.isfile(filepath):
            models.append(filepath)

    return redirect(url_for('prediction'))

@app.route('/predict', methods=['POST', 'GET'])
def prediction():
    if request.method == 'GET':
        model = request.form['Model']

        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)