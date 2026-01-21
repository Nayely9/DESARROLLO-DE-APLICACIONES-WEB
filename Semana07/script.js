let productos = [
    {
        nombre: "Laptop",
        precio: 850,
        descripcion: "Laptop para trabajo y estudio"
    },
    {
        nombre: "Mouse",
        precio: 15,
        descripcion: "Mouse inalámbrico"
    },
    {
        nombre: "Teclado",
        precio: 25,
        descripcion: "Teclado mecánico básico"
    }
];

const lista = document.getElementById("lista-productos");
const btnAgregar = document.getElementById("btn-agregar");

function renderizarProductos() {
    lista.innerHTML = "";

    productos.forEach(producto => {
        const li = document.createElement("li");
        li.innerHTML = `
            <strong>${producto.nombre}</strong><br>
            Precio: $${producto.precio}<br>
            ${producto.descripcion}
        `;
        lista.appendChild(li);
    });
}

btnAgregar.addEventListener("click", () => {
    const nombre = document.getElementById("nombre").value;
    const precio = document.getElementById("precio").value;
    const descripcion = document.getElementById("descripcion").value;

    if (nombre === "" || precio === "" || descripcion === "") {
        alert("Por favor complete todos los campos");
        return;
    }

    const nuevoProducto = {
        nombre: nombre,
        precio: precio,
        descripcion: descripcion
    };

    productos.push(nuevoProducto);
    renderizarProductos();

    document.getElementById("nombre").value = "";
    document.getElementById("precio").value = "";
    document.getElementById("descripcion").value = "";
});

renderizarProductos();
