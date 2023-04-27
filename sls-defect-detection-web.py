from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
import os

# Flask Server
app = Flask(__name__)

@app.route('/')

# TODO add prediction using tf
def home():
    return render_template('index.html')



if __name__ == '__main__':
    app.run()