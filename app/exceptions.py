class AppException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ProductoNoEncontrado(AppException):
    pass


class ClienteNoEncontrado(AppException):
    pass


class UsuarioNoEncontrado(AppException):
    pass


class ProveedorNoEncontrado(AppException):
    pass


class VentaNoEncontrada(AppException):
    pass


class FacturaNoEncontrada(AppException):
    pass


class CajaNoEncontrada(AppException):
    pass


class StockInsuficiente(AppException):
    pass
