from flask import Flask, render_template, request, redirect, Response
from database import conectar, crear_tablas
from models import InventarioClinica
from conexion.conexion import conectar_mysql
import json
import csv
import io

app = Flask(__name__)

crear_tablas()

inventario = InventarioClinica()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/medicamentos")
def listar_medicamentos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM medicamentos")
    medicamentos_db = cursor.fetchall()
    conexion.close()

    inventario.cargar_desde_db(medicamentos_db)

    return render_template(
        "medicamentos.html",
        medicamentos=inventario.mostrar_todos()
    )

@app.route("/agregar", methods=["GET", "POST"])
def agregar_medicamento():
    if request.method == "POST":
        nombre = request.form["nombre"]
        cantidad = request.form["cantidad"]
        precio = request.form["precio"]
        proveedor = request.form["proveedor"]

        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO medicamentos (nombre, cantidad, precio, proveedor) VALUES (?, ?, ?, ?)",
            (nombre, cantidad, precio, proveedor)
        )
        conexion.commit()
        conexion.close()

        return redirect("/medicamentos")

    return render_template("agregar_medicamento.html")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_medicamento(id):
    conexion = conectar()
    cursor = conexion.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        cantidad = request.form["cantidad"]
        precio = request.form["precio"]
        proveedor = request.form["proveedor"]

        cursor.execute(
            "UPDATE medicamentos SET nombre=?, cantidad=?, precio=?, proveedor=? WHERE id=?",
            (nombre, cantidad, precio, proveedor, id)
        )
        conexion.commit()
        conexion.close()

        return redirect("/medicamentos")

    cursor.execute("SELECT * FROM medicamentos WHERE id=?", (id,))
    medicamento = cursor.fetchone()
    conexion.close()

    return render_template("editar_medicamento.html", medicamento=medicamento)

@app.route("/eliminar/<int:id>")
def eliminar_medicamento(id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM medicamentos WHERE id=?", (id,))
    conexion.commit()
    conexion.close()
    return redirect("/medicamentos")

@app.route("/ver_datos")
def ver_datos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM medicamentos")
    medicamentos = cursor.fetchall()
    conexion.close()

    datos = [dict(m) for m in medicamentos]

    return render_template("ver_datos.html", datos=datos)

@app.route("/exportar/json")
def exportar_json():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM medicamentos")
    medicamentos = cursor.fetchall()
    conexion.close()

    datos = [dict(m) for m in medicamentos]

    response = Response(
        json.dumps(datos, indent=4),
        mimetype="application/json"
    )
    response.headers["Content-Disposition"] = "attachment; filename=medicamentos.json"
    return response

@app.route("/exportar/csv")
def exportar_csv():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM medicamentos")
    medicamentos = cursor.fetchall()
    conexion.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Nombre", "Cantidad", "Precio", "Proveedor"])

    for m in medicamentos:
        writer.writerow([m["id"], m["nombre"], m["cantidad"], m["precio"], m["proveedor"]])

    response = Response(
        output.getvalue(),
        mimetype="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=medicamentos.csv"
    return response


@app.route("/usuarios_mysql")
def usuarios_mysql():
    conexion = conectar_mysql()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    conexion.close()

    return render_template("usuarios_mysql.html", usuarios=usuarios)


@app.route("/agregar_usuario", methods=["GET", "POST"])
def agregar_usuario():
    if request.method == "POST":
        nombre = request.form["nombre"]
        mail = request.form["mail"]
        password = request.form["password"]

        conexion = conectar_mysql()
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)",
            (nombre, mail, password)
        )

        conexion.commit()
        conexion.close()

        return redirect("/usuarios_mysql")

    return render_template("agregar_usuario_mysql.html")


if __name__ == "__main__":
    app.run(debug=True)