from flask import Flask, render_template, request, redirect
from database import conectar, crear_tablas
from models import InventarioClinica

app = Flask(__name__)

crear_tablas()

inventario = InventarioClinica()


def cargar_medicamentos():
    conexion = conectar()
    medicamentos_db = conexion.execute("SELECT * FROM medicamentos").fetchall()
    conexion.close()
    inventario.cargar_desde_db(medicamentos_db)



@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/cita')
def cita():
    return render_template("cita.html")


@app.route('/usuario')
def usuario():
    return render_template("usuario.html")


# ============================
# MODULO INVENTARIO CLINICA
# ============================

@app.route('/medicamentos')
def medicamentos():
    cargar_medicamentos()
    lista = inventario.mostrar_todos()
    return render_template("medicamentos.html", medicamentos=lista)


@app.route('/agregar', methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        nombre = request.form["nombre"]
        cantidad = request.form["cantidad"]
        precio = request.form["precio"]
        proveedor = request.form["proveedor"]

        conexion = conectar()
        conexion.execute(
            "INSERT INTO medicamentos (nombre, cantidad, precio, proveedor) VALUES (?, ?, ?, ?)",
            (nombre, cantidad, precio, proveedor)
        )
        conexion.commit()
        conexion.close()

        return redirect("/medicamentos")

    return render_template("agregar_medicamento.html")


@app.route('/editar/<int:id>', methods=["GET", "POST"])
def editar(id):
    conexion = conectar()

    if request.method == "POST":
        nombre = request.form["nombre"]
        cantidad = request.form["cantidad"]
        precio = request.form["precio"]
        proveedor = request.form["proveedor"]

        conexion.execute(
            "UPDATE medicamentos SET nombre=?, cantidad=?, precio=?, proveedor=? WHERE id=?",
            (nombre, cantidad, precio, proveedor, id)
        )
        conexion.commit()
        conexion.close()

        return redirect("/medicamentos")

    medicamento = conexion.execute(
        "SELECT * FROM medicamentos WHERE id=?", (id,)
    ).fetchone()
    conexion.close()

    return render_template("editar_medicamento.html", medicamento=medicamento)


@app.route('/eliminar/<int:id>')
def eliminar(id):
    conexion = conectar()
    conexion.execute("DELETE FROM medicamentos WHERE id=?", (id,))
    conexion.commit()
    conexion.close()

    return redirect("/medicamentos")


if __name__ == "__main__":
    app.run(debug=True)