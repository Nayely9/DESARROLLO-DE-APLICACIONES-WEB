const nombre = document.getElementById("nombre");
const correo = document.getElementById("correo");
const password = document.getElementById("password");
const confirmar = document.getElementById("confirmar");
const edad = document.getElementById("edad");
const enviar = document.getElementById("enviar");

const errorNombre = document.getElementById("errorNombre");
const errorCorreo = document.getElementById("errorCorreo");
const errorPassword = document.getElementById("errorPassword");
const errorConfirmar = document.getElementById("errorConfirmar");
const errorEdad = document.getElementById("errorEdad");

function validarNombre() {
    if (nombre.value.length < 3) {
        errorNombre.textContent = "Debe tener al menos 3 caracteres";
        nombre.classList.add("invalido");
        nombre.classList.remove("valido");
        return false;
    }
    errorNombre.textContent = "";
    nombre.classList.add("valido");
    nombre.classList.remove("invalido");
    return true;
}

function validarCorreo() {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regex.test(correo.value)) {
        errorCorreo.textContent = "Correo no válido";
        correo.classList.add("invalido");
        correo.classList.remove("valido");
        return false;
    }
    errorCorreo.textContent = "";
    correo.classList.add("valido");
    correo.classList.remove("invalido");
    return true;
}

function validarPassword() {
    const regex = /^(?=.*[0-9])(?=.*[!@#$%^&*])/;
    if (password.value.length < 8 || !regex.test(password.value)) {
        errorPassword.textContent = "Mínimo 8 caracteres, un número y un símbolo";
        password.classList.add("invalido");
        password.classList.remove("valido");
        return false;
    }
    errorPassword.textContent = "";
    password.classList.add("valido");
    password.classList.remove("invalido");
    return true;
}

function validarConfirmacion() {
    if (password.value !== confirmar.value || confirmar.value === "") {
        errorConfirmar.textContent = "Las contraseñas no coinciden";
        confirmar.classList.add("invalido");
        confirmar.classList.remove("valido");
        return false;
    }
    errorConfirmar.textContent = "";
    confirmar.classList.add("valido");
    confirmar.classList.remove("invalido");
    return true;
}

function validarEdad() {
    if (edad.value < 18) {
        errorEdad.textContent = "Debe ser mayor o igual a 18 años";
        edad.classList.add("invalido");
        edad.classList.remove("valido");
        return false;
    }
    errorEdad.textContent = "";
    edad.classList.add("valido");
    edad.classList.remove("invalido");
    return true;
}

function validarFormulario() {
    if (
        validarNombre() &&
        validarCorreo() &&
        validarPassword() &&
        validarConfirmacion() &&
        validarEdad()
    ) {
        enviar.disabled = false;
    } else {
        enviar.disabled = true;
    }
}

nombre.addEventListener("input", validarFormulario);
correo.addEventListener("input", validarFormulario);
password.addEventListener("input", validarFormulario);
confirmar.addEventListener("input", validarFormulario);
edad.addEventListener("input", validarFormulario);

document.getElementById("formulario").addEventListener("submit", function (e) {
    e.preventDefault();
    alert("Formulario validado correctamente ✔️");
});
