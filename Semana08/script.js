document.getElementById("alertButton").addEventListener("click", function() {
  alert("Esta es una alerta");
});

document.getElementById("contactForm").addEventListener("submit", function(event) {
  let isValid = true;

  const name = document.getElementById("name");
  const email = document.getElementById("email");
  const message = document.getElementById("message");

  if (name.value.trim() === "") {
    name.classList.add("is-invalid");
    isValid = false;
  } else {
    name.classList.remove("is-invalid");
  }

  const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
  if (!email.value.match(emailPattern)) {
    email.classList.add("is-invalid");
    isValid = false;
  } else {
    email.classList.remove("is-invalid");
  }

  if (message.value.trim() === "") {
    message.classList.add("is-invalid");
    isValid = false;
  } else {
    message.classList.remove("is-invalid");
  }

  if (!isValid) {
    event.preventDefault(); 
  }
  else {
  event.preventDefault(); 
  alert("Tu mensaje ha sido enviado correctamente");
  name.value = "";
  email.value = "";
  message.value = "";
}
});
