import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Libro(db.Model):
    __tablename__ = 'libros'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('autores.id'))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    fecha_de_publicacion = db.Column(db.DateTime, default=datetime.datetime.now)
    imagen = db.Column(db.Text, nullable=False)

class Autor(db.Model):
    __tablename__ = 'autores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    libros = db.relationship("Libro", backref="autor")

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    libros = db.relationship("Libro", backref="categoria")