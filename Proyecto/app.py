from flask import Flask

app = Flask(__name__)

@app.route('/')
def inicio():
    return 'Bienvenido al Sistema de Citas Médicas – Clínica XYZ'

@app.route('/cita/<paciente>')
def cita(paciente):
    return f'Bienvenido, {paciente}. Tu cita médica está en proceso.'

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Bienvenido al sistema, {nombre}.'

if __name__ == '__main__':
    app.run(debug=True)
