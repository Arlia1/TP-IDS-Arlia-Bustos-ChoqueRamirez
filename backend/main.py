from flask import Flask, request, jsonify
from flask_cors import CORS
from time import sleep
from models import db, Libro, Autor, Categoria
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
        libros = Libro.query.order_by(Libro.id).all()
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
    except:
        return jsonify({'mensaje': 'Error interno del servidor'}), 500

@app.route("/libros/<id>", methods=['GET'])
def libro_por_id(id):
    try:
        #Aca realizo un join entre libro, autor y categoria, y lo filtro por el id del libro
        libro_info = db.session.query(Libro, Autor, Categoria).\
            join(Autor, Libro.autor_id == Autor.id).\
            join(Categoria, Libro.categoria_id == Categoria.id).\
            filter(Libro.id == id).\
            first()

        libro, autor, categoria = libro_info
        libro_data = []
        libro_data = {
            'id': libro.id,
            'titulo': libro.titulo,
            'categoria': categoria.nombre,
            'autor': autor.nombre,
            'fecha_publicacion': libro.fecha_de_publicacion.strftime('%Y-%m-%d'),
            'imagen': libro.imagen
        }
        return jsonify(libro_data)
    except:
        return jsonify({"mensaje": "Error al obtener el libro"}), 500


@app.route("/libros/<id>", methods=["DELETE"])
def eliminar_libro_por_id(id):
    try:
        libro = Libro.query.filter_by(id=id).first()
        if libro:
            db.session.delete(libro)
            db.session.commit()
            return jsonify({"success": True, "mensaje": "Libro con id {id} eliminado exitosamente"}), 200
        else:
            return jsonify({"success": False, "mensaje": "No se encontró un libro con id {id}"}), 404
    except:
        return jsonify({"success": False, "mensaje": "Error interno del servidor"}), 500

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', debug=True, port=port)
#DESCOMENTAR ESTO Y COMENTAR LO DE ABAJO PARA CARGAR BASE DE DATOS

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)