from flask_login import UserMixin

class Medicamento:
    def __init__(self, id, nombre, cantidad, precio, proveedor):
        self._id = id
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio
        self._proveedor = proveedor

    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def get_cantidad(self):
        return self._cantidad

    def get_precio(self):
        return self._precio

    def get_proveedor(self):
        return self._proveedor

    def set_cantidad(self, cantidad):
        self._cantidad = cantidad

    def set_precio(self, precio):
        self._precio = precio


class InventarioClinica:
    def __init__(self):
        self.medicamentos = {}
        self.proveedores = set()

    def cargar_desde_db(self, medicamentos_db):
        self.medicamentos.clear()
        self.proveedores.clear()

        for m in medicamentos_db:
            medicamento = Medicamento(
                m["id"],
                m["nombre"],
                m["cantidad"],
                m["precio"],
                m["proveedor"]
            )
            self.medicamentos[m["id"]] = medicamento
            self.proveedores.add(m["proveedor"])

    def mostrar_todos(self):
        return list(self.medicamentos.values())

    def buscar_por_nombre(self, nombre):
        return [
            m for m in self.medicamentos.values()
            if nombre.lower() in m.get_nombre().lower()
        ]

    def obtener_ids(self):
        return tuple(self.medicamentos.keys())


class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, email, password):
        self.id = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password