from flask import Flask, request, jsonify
from flask_cors import CORS
from time import sleep
from models import db, Libros, Autores, Categorias
from inicializar_db import initialize_database

app = Flask(__name__)
CORS(app)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://postgres:postgres@localhost:5432/tp1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#initialize_database(app)
#DESCOMENTAR ESTO PARA CARGAR BASE DE DATOS

@app.route("/")
def libros_populares():
    return "Hola mundo!"

@app.route('/libros/', methods=['GET'])
def obtener_libros():
    try:
        libros = Libros.query.order_by(Libros.id).all()
        libros_data = []
        for libro in libros:
            libro_data = {
                'id': libro.id,
                'titulo': libro.titulo,
                'autor_id': libro.autor_id,
                'categoria_id': libro.categoria_id,
                'fecha_de_publicacion': libro.fecha_de_publicacion.strftime("%Y-%m-%d"),
                'imagen': libro.imagen
            }
            libros_data.append(libro_data)
        return jsonify(libros_data)
    except Exception as error:
        print('Error:', error)
        return jsonify({'mensaje': 'Error interno del servidor'}), 500

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', debug=True, port=port)
#DESCOMENTAR ESTO Y COMENTAR LO DE ABAJO PARA CARGAR BASE DE DATOS

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)