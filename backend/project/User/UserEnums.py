from enum import Enum

class UserRoleEnum(Enum):
    administrador = 1
    usuario = 2
    aprobador = 3
    administrador_conexiones = 4
    auditor = 5
    soporte = 6
    superusuario = 7