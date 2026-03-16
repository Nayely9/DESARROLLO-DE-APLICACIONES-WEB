from flask import Flask, render_template, request, redirect, Response, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from database import conectar, crear_tablas
from models import InventarioClinica, Usuario
from conexion.conexion import conectar_mysql
import json
import csv
import io

app = Flask(__name__)
app.secret_key = "secreto"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

crear_tablas()

inventario = InventarioClinica()


@login_manager.user_loader
def load_user(user_id):
    conexion = conectar_mysql()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE id_usuario=%s", (user_id,))
    user = cursor.fetchone()

    conexion.close()

    if user:
        return Usuario(user["id_usuario"], user["nombre"], user["email"], user["password"])
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conexion = conectar_mysql()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
        "SELECT * FROM usuarios WHERE email=%s AND password=%s",
        (email,password)
        )

        user = cursor.fetchone()

        conexion.close()

        if user:
            usuario = Usuario(user["id_usuario"],user["nombre"],user["email"],user["password"])
            login_user(usuario)
            return redirect("/panel")

    return render_template("login.html")


@app.route("/registro", methods=["GET","POST"])
def registro():

    if request.method == "POST":

        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]

        conexion = conectar_mysql()
        cursor = conexion.cursor()

        cursor.execute(
        "INSERT INTO usuarios(nombre,email,password) VALUES(%s,%s,%s)",
        (nombre,email,password)
        )

        conexion.commit()
        conexion.close()

        return redirect("/login")

    return render_template("registro.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/panel")
@login_required
def panel():
    return render_template("panel.html", nombre=current_user.nombre)


@app.route("/medicamentos")
@login_required
def listar_medicamentos():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM medicamentos")

    medicamentos_db = cursor.fetchall()

    conexion.close()

    inventario.cargar_desde_db(medicamentos_db)

    return render_template("medicamentos.html", medicamentos=inventario.mostrar_todos())


@app.route("/agregar", methods=["GET","POST"])
@login_required
def agregar_medicamento():

    if request.method == "POST":

        nombre = request.form["nombre"]
        cantidad = request.form["cantidad"]
        precio = request.form["precio"]
        proveedor = request.form["proveedor"]

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute(
        "INSERT INTO medicamentos (nombre,cantidad,precio,proveedor) VALUES (?,?,?,?)",
        (nombre,cantidad,precio,proveedor)
        )

        conexion.commit()
        conexion.close()

        return redirect("/medicamentos")

    return render_template("agregar_medicamento.html")


@app.route("/ver_datos")
@login_required
def ver_datos():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM medicamentos")

    medicamentos = cursor.fetchall()

    conexion.close()

    datos = [dict(m) for m in medicamentos]

    return render_template("ver_datos.html", datos=datos)


@app.route("/usuarios_mysql")
@login_required
def usuarios_mysql():

    conexion = conectar_mysql()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios")

    usuarios = cursor.fetchall()

    conexion.close()

    return render_template("usuarios_mysql.html", usuarios=usuarios)


if __name__ == "__main__":
    app.run(debug=True)