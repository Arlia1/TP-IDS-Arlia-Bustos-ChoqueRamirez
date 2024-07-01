from flask import Flask, request, jsonify
from flask_cors import CORS
from time import sleep
from models import db, Libro, Autor, Categoria
from inicializar_db import initialize_database
import sys

app = Flask(__name__)
CORS(app)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://postgres:postgres@localhost:5432/tp1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

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

@app.route("/libros/categoria/<int:categoria_id>", methods=['GET'])
def obtener_libros_por_categoria(categoria_id):
    try:
        libros = Libro.query.filter_by(categoria_id=categoria_id).all()
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
    sleep(1.5)
    try:
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

@app.route("/libros/", methods=['POST'])
def agregar_libro():
    try:
        data = request.json
        nuevo_titulo = data.get('titulo')
        nuevo_categoria_nombre = data.get('categoria')
        nuevo_autor_nombre = data.get('autor')
        nueva_fecha_publicacion = data.get('fecha_de_publicacion')
        nueva_imagen = data.get('imagen')

        
        categoria = Categoria.query.filter_by(nombre=nuevo_categoria_nombre).first()
        
        if not categoria:
            categoria = Categoria(nombre=nuevo_categoria_nombre)
            db.session.add(categoria)
            db.session.commit()

        
        autor = Autor.query.filter_by(nombre=nuevo_autor_nombre).first()
        
        if not autor:
            autor = Autor(nombre=nuevo_autor_nombre)
            db.session.add(autor)
            db.session.commit()

        
        nuevo_libro = Libro(titulo=nuevo_titulo, categoria_id=categoria.id, autor_id=autor.id, fecha_de_publicacion=nueva_fecha_publicacion ,imagen=nueva_imagen)
        db.session.add(nuevo_libro)
        db.session.commit()

        return jsonify({
            'libro': {
                'id': nuevo_libro.id,
                'titulo': nuevo_libro.titulo,
                'categoria': nuevo_libro.categoria.nombre,
                'autor': nuevo_libro.autor.nombre,
                'imagen': nuevo_libro.imagen
            }
        }), 201
    except:
        return jsonify({'mensaje': 'Error al agregar libro'}), 500


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

@app.route("/libros/<id>", methods=["PUT"])
def editar_libro_por_id(id):
    try:
        data = request.json
        nuevo_titulo = data.get('titulo')
        nuevo_autor_nombre = data.get('autor')
        
        nuevo_categoria_nombre = data.get('categoria')
        
        nueva_fecha_publicacion = data.get('fecha_publicacion')
        
        nueva_imagen = data.get('imagen')
        
        libro = Libro.query.filter_by(id=id).first()
        
        if libro:
            
            if nuevo_titulo:
                libro.titulo = nuevo_titulo
            
            if nuevo_categoria_nombre:
                categoria = Categoria.query.filter_by(nombre=nuevo_categoria_nombre).first()
                if not categoria:
                    categoria = Categoria(nombre=nuevo_categoria_nombre)
                    db.session.add(categoria)
                    db.session.commit()
                libro.categoria_id = categoria.id
            
            if nuevo_autor_nombre:
                autor = Autor.query.filter_by(nombre=nuevo_autor_nombre).first()
                if not autor:
                    autor = Autor(nombre=nuevo_autor_nombre)
                    db.session.add(autor)
                    db.session.commit()
                libro.autor_id = autor.id
           
            if nueva_fecha_publicacion:
                libro.fecha_de_publicacion = nueva_fecha_publicacion
            
            if nueva_imagen:
                libro.imagen = nueva_imagen
            
            db.session.commit()
            
            return jsonify({
                'libro': {
                    'id': libro.id,
                    'titulo': libro.titulo,
                    'categoria': libro.categoria.nombre,
                    'autor': libro.autor.nombre,
                    'fecha_publicacion': libro.fecha_de_publicacion.strftime('%Y-%m-%d'),
                    'imagen': libro.imagen
                }
            }), 200
        else:
            return jsonify({"mensaje": f"No se encontró un libro con id {id}"}), 404
    except:
        return jsonify({"mensaje": "Error al editar el libro"}), 500

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()

    if len(sys.argv) > 1:
        if (sys.argv[1] == "--init"):
            initialize_database(app)
    
    app.run(host='0.0.0.0', debug=True, port=port)