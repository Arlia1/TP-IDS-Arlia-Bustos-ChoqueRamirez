from flask import Flask, request
from flask_cors import CORS
from time import sleep

app = Flask(__name__)
CORS(app)

@app.route("/")
def libros_populares():
    return "Hola mundo!"