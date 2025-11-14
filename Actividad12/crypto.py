# Importar las clases necesarias de la librería cryptography
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# default_backend es necesario para inicializar el objeto Cipher
from cryptography.hazmat.backends import default_backend
# urandom se utiliza para generar bytes aleatorios criptográficamente seguros para la clave y el IV
from os import urandom

def generar_clave_y_iv():
    """
    Genera una clave y un vector de inicialización (IV) aleatorios.
    La clave es de 32 bytes para usar AES-256 (el cifrado más fuerte de AES).
    El IV es de 16 bytes, que es el tamaño del bloque para AES.
    """
    # 32 bytes = 256 bits, para el algoritmo AES-256
    key = urandom(32)
    # 16 bytes = 128 bits, que es el tamaño del bloque de AES, requerido para el IV en modo CBC
    iv = urandom(16)
    return key, iv

def encriptar(texto_plano, key, iv):
    """
    Cifra el texto plano usando el algoritmo AES en modo CBC (Cipher Block Chaining).

    :param texto_plano: El texto a cifrar (string).
    :param key: La clave secreta (bytes).
    :param iv: El vector de inicialización (bytes).
    :return: El texto cifrado (bytes).
    """
    # Inicializa el objeto Cipher: especifica el algoritmo (AES con la clave) y el modo de operación (CBC con el IV)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    # Crea el objeto que realiza la encriptación
    encryptor = cipher.encryptor()

    # El modo CBC requiere que la longitud de los datos sea un múltiplo exacto del tamaño del bloque (16 bytes).
    texto_plano_bytes = texto_plano.encode('utf-8')
    # Calcula cuántos bytes de relleno se necesitan
    padding_length = 16 - (len(texto_plano_bytes) % 16)
    # Crea los bytes de relleno: repite el valor de padding_length (según PKCS#7)
    padding = bytes([padding_length] * padding_length)
    # Concatena el texto original con el relleno
    texto_a_cifrar = texto_plano_bytes + padding

    # Realiza la encriptación: update() procesa los datos, finalize() maneja el posible estado interno y asegura el final.
    texto_cifrado = encryptor.update(texto_a_cifrar) + encryptor.finalize()
    return texto_cifrado

def desencriptar(texto_cifrado, key, iv):
    """
    Descifra el texto cifrado usando el algoritmo AES en modo CBC.

    :param texto_cifrado: El texto cifrado (bytes).
    :param key: La clave secreta (bytes).
    :param iv: El vector de inicialización (bytes).
    :return: El texto descifrado y sin relleno (string).
    """
    # Inicializa el objeto Cipher (igual que en encriptar)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    # Crea el objeto que realiza la desencriptación
    decryptor = cipher.decryptor()
    
    # Descifra todo el texto. El resultado aún contiene el padding.
    texto_descifrado_con_padding = decryptor.update(texto_cifrado) + decryptor.finalize()

    # --- Eliminación manual de PKCS#7 Padding ---
    # El último byte indica la longitud del relleno
    padding_length = texto_descifrado_con_padding[-1]
    # Retorna la cadena sin los últimos 'padding_length' bytes
    texto_descifrado = texto_descifrado_con_padding[:-padding_length]
    
    # Decodifica los bytes descifrados de nuevo a un string (utf-8)
    return texto_descifrado.decode('utf-8')

# --- Bloque de Uso y Prueba ---

# 1. Generar clave y IV. **NOTA**: Para un uso real, la clave y el IV deben
#    almacenarse de forma segura y compartirse de forma independiente.
key, iv = generar_clave_y_iv()

# 2. Texto original (string)
texto_original = "Edgar Antonio Torres Saavedra, la cabra."

print("Texto original:", texto_original)
print("Clave (bytes):", key.hex()) # Muestra la clave en formato hexadecimal para inspección
print("IV (bytes):", iv.hex())     # Muestra el IV en formato hexadecimal para inspección
print("-" * 20)

# 3. Encriptar el mensaje
texto_encriptado = encriptar(texto_original, key, iv)
# El texto cifrado se muestra como bytes, lo cual es ilegible
print("Texto encriptado (bytes):", texto_encriptado)
# A menudo, el texto cifrado se convierte a Base64 o Hexadecimal para ser transmitido o almacenado como texto
print("Texto encriptado (hex):", texto_encriptado.hex())
print("-" * 20)

# 4. Desencriptar el mensaje
# Se necesita exactamente la misma 'key' y el mismo 'iv'
texto_desencriptado = desencriptar(texto_encriptado, key, iv)
print("Texto desencriptado:", texto_desencriptado)