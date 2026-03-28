class ProductoForm:
    def __init__(self, form):
        self.nombre = form.get("nombre")
        self.precio = form.get("precio")
        self.stock = form.get("stock")