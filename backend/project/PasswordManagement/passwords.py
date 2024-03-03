import hashlib

def generar_hash_contrasena(contrasena):
    """
    Genera el hash de una contraseña utilizando SHA-256.

    Parámetros:
        contrasena: La contraseña a hashear.

    Retorno:
        El hash de la contraseña en formato hexadecimal.
    """
    hash_bytes = hashlib.sha256(contrasena.encode('utf-8')).digest()
    return hash_bytes.hex()


def verificar_contrasena(contrasena_ingresada, hash_contrasena):
  """
  Verifica si la contraseña ingresada coincide con el hash almacenado.

  Parámetros:
    contrasena_ingresada: La contraseña ingresada por el usuario.
    hash_contrasena: El hash de la contraseña almacenado en la base de datos.

  Retorno:
    True si la contraseña coincide, False en caso contrario.
  """
  contrasena_ingresada_hash = hashlib.sha256(contrasena_ingresada.encode('utf-8')).digest().hex()
  return hash_contrasena == contrasena_ingresada_hash