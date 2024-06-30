## Padron: 111520, Nombre: Yoel Gaston Arlia, Mail: arliayoel23@gmail.com

## Padron: 110759, Nombre: Franco Bustos, Mail: francoabustos1508@gmail.com

## Padron: 110895, Nombre: Emanuel Choque Ramirez, Mail: emanuel.chrz08@gmail.com

# TP-IDS-Arlia-Bustos-ChoqueRamirez
La página es una galería de imágenes de biblioteca que permite a los usuarios visualizar, editar, eliminar y agregar libros. Esta aplicación web se estructura en una arquitectura de cliente-servidor, donde el frontend y el backend interactúan para proporcionar una experiencia de usuario fluida y funcional. A continuación, se detalla el uso y la función de cada componente tecnológico involucrado en el proyecto:
### Frontend
>>El frontend está desarrollado utilizando HTML, CSS, Bootstrap y JavaScript. HTML estructura el contenido de la página, mientras que CSS y Bootstrap se utilizan para diseñar y asegurar una interfaz responsiva y atractiva. JavaScript mejora la interactividad de la página, permitiendo a los usuarios interactuar dinámicamente con los datos presentados sin necesidad de recargar la página.
### Backend
>>El backend está implementado en Python con el framework Flask. Flask procesa las solicitudes HTTP, ejecuta la lógica de la aplicación (como la gestión de libros), y comunica con la base de datos para recuperar o modificar la información. El backend sirve como el puente entre el frontend y la base de datos, asegurando que los datos mostrados al usuario estén actualizados y sean consistentes.
### Base de Datos (BDD)
>>La persistencia de datos se maneja a través de PostgreSQL, una base de datos relacional que almacena toda la información de los libros. SQLAlchemy, ara Python, se utiliza para facilitar la interacción con la base de datos. Esto permite realizar consultas y operaciones sobre la base de datos de manera segura y eficiente, utilizando código Python en lugar de SQL directo.
### Bash y GitHub
>>Bash se utiliza para la automatización de tareas y la gestión del entorno de desarrollo, como la activación de entornos virtuales, la instalación de dependencias y la ejecución de la aplicación. GitHub es la plataforma de control de versiones elegida para este proyecto, permitiendo un desarrollo colaborativo y el seguimiento de cambios en el código fuente. GitHub facilita la colaboración entre desarrolladores y la integración continua del proyecto.

### Prerrequisitos
Qué cosas necesitas para instalar el software y cómo instalarlas:

```bash
pip3 install -r src/requirements.txt
```
Para inicializar una base de datos con libros por default:
```bash
cd backend/ && python3 main.py --init
```

Cosas que necesitas correr para que funcione el proyecto: 

```bash
cd frontend/ && python3 -m http.server
cd backend/ && python3 main.py
```
### Diagrama de las tablas de la base de datos.
<div>
    <img src="img/Diagrama ERN.png"></img>
</div>
