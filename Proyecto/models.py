class Medicamento:
    def __init__(self, id, nombre, cantidad, precio, proveedor):
        self._id = id
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio
        self._proveedor = proveedor

    # GETTERS
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

    # SETTERS
    def set_cantidad(self, cantidad):
        self._cantidad = cantidad

    def set_precio(self, precio):
        self._precio = precio


class InventarioClinica:
    def __init__(self):
        # Diccionario para búsqueda rápida por ID
        self.medicamentos = {}

        # Conjunto para proveedores únicos
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
        # Devuelve una lista
        return list(self.medicamentos.values())

    def buscar_por_nombre(self, nombre):
        return [
            m for m in self.medicamentos.values()
            if nombre.lower() in m.get_nombre().lower()
        ]

    def obtener_ids(self):
        # Devuelve una tupla
        return tuple(self.medicamentos.keys())