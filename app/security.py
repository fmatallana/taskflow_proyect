# Para manejar las contraseñas, passlib utiliza algo llamado "Contexto de Criptografía" (CryptContext) Este contexto es básicamente el motor que sabe qué algoritmo usar (en nuestro caso, bcrypt) y cómo hacer los cálculos matemáticos para encriptar.

from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

SECRET_KEY = "98U9EOPDIJASDSNKJ0324R"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# las variables de la linea 5 a la 7 son necesarias para crear un  Token JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
"""
Una clave secreta (SECRET_KEY): Una frase súper larga y difícil que solo tu servidor conoce. Sirve para firmar los tokens y evitar que alguien invente uno falso.

Un algoritmo (ALGORITHM): El método matemático para firmarlo (el estándar en la industria es "HS256").

Un tiempo de expiración (ACCESS_TOKEN_EXPIRE_MINUTES): Cuánto tiempo será válido el token antes de que el usuario tenga que volver a hacer login (por ejemplo, 30 minutos).
"""
# Configuramos el motor para usar bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encriptar_contrasena(password):
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verificacion_de_contrasena(password_text_plain, hashed_password):
    verification = pwd_context.verify(password_text_plain, hashed_password)
    return verification


def crear_token_acceso(datos: dict):
    # 1. Hacemos una copia para no modificar los datos originales por accidente
    datos_a_codificar = datos.copy()

    # 2. Calculamos cuándo expira (ahora + 30 minutos)
    expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # 3. Agregamos la fecha de expiración al diccionario de datos
    datos_a_codificar.update({"exp": expiracion})
    token = jwt.encode(datos_a_codificar, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verificar_token(token: str):
    datos_decodificados = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return datos_decodificados
    # jwt.decode(...): Esta es la herramienta principal. Hace el trabajo inverso a la creación del token. Intenta "abrir" el paquete cifrado para ver qué hay dentro. 📦
    # En resumen: la función toma la cadena cifrada, verifica que nuestra firma sea válida y, si lo es, nos devuelve la información del usuario que estaba oculta dentro.


def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    try:
        # PASO 1: Usa tu función 'verificar_token' pasándole la variable 'token'
        # y guarda el resultado en una variable llamada 'payload'.
        payload = verificar_token(token)

        # PASO 2: Extrae el nombre de usuario del 'payload' usando la llave "sub"
        # y guárdalo en una variable llamada 'username'.

        username = payload.get("sub")
        # --- El resto del código te protege de errores ---
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se pudo validar las credenciales",
            )
        return username

    except jwt.PyJWTError:  # Esto atrapa tokens vencidos o falsos
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado"
        )
