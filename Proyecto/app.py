from flask import Flask, render_template

app = Flask(__name__)

# Página principal
@app.route('/')
def inicio():
    return render_template('index.html')

# Página acerca de
@app.route('/about')
def about():
    return render_template('about.html')

# Ruta dinámica cita
@app.route('/cita/<paciente>')
def cita(paciente):
    return render_template('cita.html', paciente=paciente)

# Ruta dinámica usuario
@app.route('/usuario/<nombre>')
def usuario(nombre):
    return render_template('usuario.html', nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True) 