import csv, json
from io import StringIO, BytesIO
from decimal import Decimal
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# ReportLab para el PDF Profesional
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from conexion.conexion import conectar_mysql
from models.usuario import Usuario
from services.producto_service import *
from services.paciente_service import *
from services.asignacion_service import *

app = Flask(__name__)
app.secret_key = "clinica_ny_2026"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# --- CLASE PARA EVITAR ERROR DE JSON CON PRECIOS (DECIMAL) ---
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

@login_manager.user_loader
def load_user(user_id):
    db = conectar_mysql()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario=%s", (user_id,))
    user = cursor.fetchone()
    db.close()
    if user:
        return Usuario(user["id_usuario"], user["nombre"], user["email"], user["password"])
    return None

# --- RUTAS DE NAVEGACIÓN ---

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password_plana = request.form["password"]
        db = conectar_mysql()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        user = cursor.fetchone()
        db.close()
        if user and check_password_hash(user["password"], password_plana):
            usuario = Usuario(user["id_usuario"], user["nombre"], user["email"], user["password"])
            login_user(usuario)
            return redirect(url_for("panel"))
        flash("Correo o contraseña incorrectos")
    return render_template("login.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        db = conectar_mysql()
        cursor = db.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", (nombre, email, password))
        db.commit()
        db.close()
        return redirect(url_for("login"))
    return render_template("registro.html")

@app.route("/panel")
@login_required
def panel():
    return render_template("panel.html", nombre=current_user.nombre)

@app.route("/sobre_nosotros")
def sobre_nosotros():
    return render_template("sobre_nosotros.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

# --- REPORTES (NOMBRES UNIFICADOS PARA EVITAR BUILDERROR) ---

@app.route("/descargar/json")
@login_required
def productos_json():
    lista = listar_medicamentos()
    return Response(json.dumps(lista, indent=4, cls=DecimalEncoder), 
                    mimetype="application/json", 
                    headers={"Content-disposition": "attachment; filename=reporte.json"})

@app.route("/descargar/csv")
@login_required
def productos_csv():
    lista = listar_medicamentos()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['#', 'Medicamento', 'Precio', 'Stock'])
    for i, p in enumerate(lista, 1):
        cw.writerow([i, p['nombre'], p['precio'], p['stock']])
    return Response(si.getvalue(), mimetype="text/csv", headers={"Content-disposition": "attachment; filename=reporte.csv"})

@app.route("/descargar/txt")
@login_required
def productos_txt():
    lista = listar_medicamentos()
    output = "REPORTE CLÍNICA NY\n" + "="*20 + "\n"
    for i, p in enumerate(lista, 1):
        output += f"{i}. {p['nombre']} - Stock: {p['stock']}\n"
    return Response(output, mimetype="text/plain", headers={"Content-disposition": "attachment; filename=reporte.txt"})

@app.route("/descargar/pdf")
@login_required
def productos_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    elements = []

# --- 1. TÍTULO PRINCIPAL ---
    # Usamos HexColor corregido para el tono azul oscuro de la imagen
    titulo_style = styles['Title']
    titulo_style.textColor = colors.HexColor('#0a2b5c')
    titulo_style.fontSize = 22
    elements.append(Paragraph("REPORTE MAESTRO - CLÍNICA NY", titulo_style))
    elements.append(Spacer(1, 10))

    # --- 2. SUBTÍTULO / FECHA ---
    subtitulo = styles['Normal']
    subtitulo.alignment = 1  # Centrado
    elements.append(Paragraph("<b>Listado General de Inventario y Medicamentos</b>", subtitulo))
    elements.append(Spacer(1, 20))

    # --- 3. DISEÑO DE LA TABLA ---
    # Los colores según tu captura de pantalla
    style_table = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0a2b5c')), # Encabezado Azul
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f2f4f7')), # Fondo gris claro para filas
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])

    # --- 4. CARGA DE DATOS ---
    data = [['ID', 'Medicamento', 'Precio Unitario', 'Stock Actual']]
    for m in listar_medicamentos():
        data.append([
            m['medicamento_id'], 
            m['nombre'], 
            f"$ {m['precio']}", 
            f"{m['stock']} u."
        ])
    
    # Ajustamos el ancho de las columnas para que ocupen la página
    t = Table(data, colWidths=[40, 220, 100, 100])
    t.setStyle(style_table)
    elements.append(t)

    # --- 5. PIE DE PÁGINA ---
    elements.append(Spacer(1, 30))
    pie = Paragraph("<font color='grey' size='9'>Generado por Sistema Gestión Clínica NY - 2026</font>", subtitulo)
    elements.append(pie)

    doc.build(elements)
    buffer.seek(0)
    return Response(buffer, mimetype="application/pdf", 
                    headers={"Content-disposition": "attachment; filename=Reporte_ClinicaNY.pdf"})

# --- SECCIONES PRINCIPALES ---

@app.route("/productos")
@login_required
def productos():
    return render_template("productos/listar.html", productos=listar_medicamentos())

@app.route("/pacientes")
@login_required
def pacientes():
    return render_template("pacientes.html", pacientes=listar_pacientes())

@app.route("/ver_asignaciones")
@login_required
def ver_asignaciones():
    return render_template("listar_asignaciones.html", asignaciones=listar_asignaciones())

# --- OPERACIONES (CRUD) ---

@app.route("/productos/crear", methods=["GET", "POST"])
@login_required
def crear_producto():
    if request.method == "POST":
        insertar_producto(request.form["nombre"], float(request.form["precio"]), int(request.form["stock"]))
        return redirect(url_for("productos"))
    return render_template("productos/crear.html")

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):
    if request.method == "POST":
        actualizar_producto(id, request.form["nombre"], float(request.form["precio"]), int(request.form["stock"]))
        return redirect(url_for("productos"))
    return render_template("productos/editar.html", producto=obtener_medicamento(id))

@app.route("/productos/eliminar/<int:id>")
@login_required
def eliminar_producto_ruta(id):
    eliminar_medicamento(id)
    return redirect(url_for("productos"))

@app.route("/pacientes/crear", methods=["GET", "POST"])
@login_required
def crear_paciente():
    if request.method == "POST":
        insertar_paciente(request.form["nombre"], request.form["email"])
        return redirect(url_for("pacientes"))
    return render_template("crear_paciente.html")

@app.route("/asignar", methods=["GET", "POST"])
@login_required
def asignar():
    if request.method == "POST":
        if registrar_asignacion(request.form.get("m_id"), request.form.get("p_id"), request.form.get("cant"), request.form.get("fecha")):
            flash("Entrega exitosa")
            return redirect(url_for("ver_asignaciones"))
        flash("Error: Stock insuficiente")
    return render_template("asignar.html", medicamentos=listar_medicamentos(), pacientes=listar_pacientes())

if __name__ == "__main__":
    app.run(debug=True)