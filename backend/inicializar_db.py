from models import db, Libro, Autor, Categoria
import datetime, csv



def initialize_database(app):
    nombre_archivo = "libros.csv"
    with app.app_context():
        with open(nombre_archivo, mode='r', newline='\n', encoding='utf-8') as archivo:
            lector = csv.reader(archivo, delimiter=';')
            
            for fila in lector:
                
                titulo = fila[0]
                nombre_autor = fila[1]
                fecha_de_publicacion = datetime.datetime.strptime(fila[2], "%Y-%m-%d")
                nombre_categoria = fila[3]
                imagen = fila[4]

                # Busca o crea el autor
                autor = Autor.query.filter_by(nombre=nombre_autor).first()
                if not autor:
                    autor = Autor(nombre=nombre_autor)  # Ajusta la edad según sea necesario
                    db.session.add(autor)

                # Busca o crea la categoría
                categoria = Categoria.query.filter_by(nombre=nombre_categoria).first()
                if not categoria:
                    categoria = Categoria(nombre=nombre_categoria)
                    db.session.add(categoria)

                # Busca o crea el libro
                libro =    Libro.query.filter_by(titulo=titulo).first()
                if not libro:
                    libro =    Libro(titulo=titulo, autor=autor, categoria=categoria, fecha_de_publicacion=fecha_de_publicacion, imagen=imagen)
                    db.session.add(libro)

            # Commit para insertar los datos en la base de datos
            db.session.commit()
        