///libros
function response_received(response) {
    return response.json();
}

function actualizar_libros() {
    const container = document.getElementById("libros");
    container.innerHTML = "";
}

function parse_data_cargar_libros(content) {
    const container = document.getElementById("libros");
    const rutaActual = window.location.pathname;
    console.log(content)

    for (let i = 0; i < content.length; i++) {
        const libro = document.createElement("div");
        libro.setAttribute("class", "col-6 col-md-4 col-lg-3 col-xl-2");

        const imagen = document.createElement("img");
        imagen.setAttribute("class", "card-img-top");
        imagen.setAttribute("src", content[i].imagen);
        imagen.setAttribute("style", "max-height: 200px;"); // Establecer altura máxima para la imagen

        const carta = document.createElement("a");
        carta.setAttribute("class", "card text-decoration-none card-custom");
        carta.setAttribute("style", "overflow: hidden;"); // Establecer altura máxima y ocultar contenido excedente

        carta_cuerpo = null
        if (rutaActual == '/libros/') {
            carta_cuerpo = document.createElement("div");
            carta.setAttribute("href", "/libros/libro?id=" + content[i].id);
            carta_cuerpo.setAttribute("class", "card-body small-text custom-padding");
        } else if (rutaActual == '/eliminar/seleccionar/') {
            carta.setAttribute("onclick", `eliminar_libro(${content[i].id}, "${content[i].titulo}")`)
            carta_cuerpo = document.createElement("button");
            carta_cuerpo.setAttribute("class", "btn btn-danger small-text no-border-radius");
            // carta_cuerpo.setAttribute("onclick", `eliminar_libro(${content[i].id}, "${content[i].titulo}")`)
        } else if (rutaActual == '/editar/seleccionar/') {
            carta_cuerpo = document.createElement("div");
            carta.setAttribute("href", "/editar/?id=" + content[i].id);
            carta_cuerpo.setAttribute("class", "card-body small-text custom-padding");
        }

        carta_cuerpo.append(content[i].titulo);
        carta.append(imagen);
        carta.append(carta_cuerpo);
        libro.append(carta);
        container.append(libro);
    }
}

function request_error_cargar_libros(error) {
    console.log("ERROR");
    console.log(error);
}

function cargar_libros() {
    fetch("http://localhost:5000/libros/")
        .then(response_received)
        .then(parse_data_cargar_libros)
        .catch(request_error_cargar_libros);
}

function filtrar_por_categoria(categoria_id) {
    actualizar_libros();

    fetch(`http://localhost:5000/libros/categoria/${categoria_id}`)
        .then(response_received)
        .then(parse_data_cargar_libros)
        .catch(request_error_cargar_libros);
}

function mostrar_todos() {
    actualizar_libros();
    cargar_libros();
}

//esto es libros/libro

function parse_data_libro(libro) {
    const loading_message = document.getElementById("loading-message");
    loading_message.remove();

    const titulo = document.getElementById("titulo")
    titulo.innerText = libro.titulo

    const imagen = document.getElementById("imagen")
    imagen.setAttribute("src", libro.imagen)
    //imagen.classList.add("img-thumbnail")
    imagen.setAttribute("class", "img-fluid img-thumbnail");

    const categoria = document.getElementById("categoria")
    categoria.innerText = `${libro.categoria}`

    const autor = document.getElementById("autor")
    autor.innerText = `${libro.autor}`

    const fecha_publicacion = document.getElementById("fecha_publicacion")
    fecha_publicacion.innerText = `${libro.fecha_publicacion}`

    const edit_btn = document.getElementById("edit-btn")
    edit_btn.href = `/editar?id=${libro.id}`

    const boton_eliminar = document.getElementById("boton-eliminar");
    boton_eliminar.addEventListener("click", function () {
        eliminar_libro(libro.id, libro.titulo);
    });
}

function handle_error_libro(error) {
    console.log("ERROR", error);
    alert("Ocurrió un error al cargar el libro");
}

function delete_response(data) {
    const rutaActual = window.location.pathname;
    if (data.success) {
        alert("El libro se elimino correctamente")
        if (rutaActual.includes('/libros/libro')) {
            window.location.href = "/libros/";
        } else if (rutaActual == '/eliminar/seleccionar/') {
            window.location.href = "/eliminar/seleccionar/";
        }
    } else {
        alert("Ocurrio un error, intenta de nuevo")
    }
}

function eliminar_libro(id, titulo) {
    const confirmacion = confirm(`Seguro que queres eliminar el libro ${titulo}?`)
    if (!confirmacion) {
        return;
    }

    fetch(
        `http://localhost:5000/libros/${id}`,
        { method: "DELETE" }
    )
        .then((res) => res.json())
        .then(delete_response)
        .catch(handle_error_eleminar_libro)
}

function handle_response_agregar_editar(data) {
    console.log(data);
    if (data.libro) {
        alert("La operacion se realizo con exito")
        const libro = data.libro;
        window.location.href = `/libros/libro?id=${libro.id}`
    } else {
        alert("Error");
    }
}

function agregar_libro(event) { // event --> submit
    event.preventDefault()

    const formData = new FormData(event.target)

    const titulo = formData.get("titulo");
    const autor = formData.get("autor");
    const categoria = formData.get("categoria");
    const fecha_publicacion = formData.get("fecha_publicacion")
    const imagen = formData.get("imagen");

    if (titulo === null || autor === null || categoria === null || categoria === "null" || fecha_publicacion === null || imagen === null) {
        alert("Por favor, complete todos los campos");
        return;
    }

    fetch("http://localhost:5000/libros/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            titulo: titulo,
            categoria: categoria,
            fecha_de_publicacion: fecha_publicacion,
            autor: autor,
            imagen: imagen
        })
    })
        .then((res) => res.json())
        .then(handle_response_agregar_editar)
        .catch((error) => console.error("ERROR", error));
}

function parse_data_editar(libro) {

    const titulo = document.getElementById("titulo")
    titulo.value = libro.titulo

    const autor = document.getElementById("autor")
    autor.value = libro.autor

    const categoria = document.getElementById("categoria")
    categoria.value = libro.categoria

    const fecha_publicacion = document.getElementById("fecha_publicacion");
    fecha_publicacion.value = libro.fecha_publicacion;

    const imagen = document.getElementById("imagen");
    imagen.value = libro.imagen;

}

function handle_error_editar(error) {
    console.log("ERROR", error);
    alert("Ocurrió un error al editar el libro");
}

function editarLibro(event){
    const params = new URLSearchParams(window.location.search)
    const id = params.get("id")

    event.preventDefault()
    const formData = new FormData(event.target)
    const titulo = formData.get("titulo");
    const autor = formData.get("autor");
    const categoria = formData.get("categoria");
    const fecha_publicacion = formData.get("fecha_publicacion")
    const imagen = formData.get("imagen");

    const confirmacion = confirm(`Seguro que queres editar el libro ${titulo}?`)
    if (!confirmacion) {
        return;
    }

    
    if (titulo === null || autor === null || categoria === null || categoria === "null" || fecha_publicacion === null || imagen === null) {
        alert("Por favor, complete todos los campos");
        return; 
    }
    
    fetch(`http://localhost:5000/libros/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            titulo: titulo,
            autor: autor,
            categoria: categoria,
            fecha_publicacion: fecha_publicacion,
            imagen: imagen
        })
    })
        .then((res) => res.json())
        .then(handle_response_agregar_editar)
        .catch(handle_error_editar)
}


function cargar_libro_editar() {
    const params = new URLSearchParams(window.location.search)
    const id = params.get("id")


    if (id === null) {
        window.location.href = "/";
    }
    
    fetch(`http://localhost:5000/libros/${id}`)
        .then(response_received)
        .then(parse_data_editar)
        .catch(handle_error_editar);
}


function cargar_libro_ver_libro() {
    const params = new URLSearchParams(window.location.search)
    const id = params.get("id")

    if (id === null) {
        window.location.href = "/"; //esto salta si la direccion es: libros/
    }

    fetch(`http://localhost:5000/libros/${id}`)
        .then(response_received)
        .then(parse_data_libro)
        .catch(handle_error_libro)
}


document.addEventListener("DOMContentLoaded", function () {
    const rutaActual = window.location.pathname;
    console.log(rutaActual);
    
    if (rutaActual == '/libros/' || rutaActual == '/eliminar/seleccionar/' || rutaActual == '/editar/seleccionar/') {
        cargar_libros();
    } else if (rutaActual.includes('/libros/libro')) {
        cargar_libro_ver_libro();
    } else if (rutaActual == '/crear/') {
        //cosas necesrias a realizar para /crear/
    } else if (rutaActual.includes('/editar/')) {
        console.log("prueba")
        cargar_libro_editar();
    } else {
        console.log(rutaActual)
    }
});
