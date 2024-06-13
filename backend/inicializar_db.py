from models import db, Libros, Autores, Categorias
import datetime

def initialize_database(app):
    db.init_app(app)
    with app.app_context():
        for i in range(1, 6):
            autor = Autores.query.filter_by(nombre=f"Autor {i}").first()
            if not autor:
                autor = Autores(nombre=f"Autor {i}", edad=20+i)
                db.session.add(autor)

            categoria = Categorias.query.filter_by(nombre=f"Categoria {i}").first()
            if not categoria:
                categoria = Categorias(nombre=f"Categoria {i}")
                db.session.add(categoria)

            libro = Libros.query.filter_by(titulo=f"Libro {i}").first()
            if not libro:
                libro = Libros(titulo=f"Libro {i}", autor=autor, categoria=categoria, fecha_de_publicacion=datetime.datetime.now(), imagen=f"imagen{i}.jpg")
                db.session.add(libro)

        # Commit para insertar los datos en la base de datos
        db.session.commit()