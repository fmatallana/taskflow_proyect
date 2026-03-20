from contextlib import asynccontextmanager

from database import create_db_and_tables
from fastapi import FastAPI

"""lifespan espera una función especial (un generador asíncrono) y no directamente la función que crea las tablas
En las versiones más modernas de FastAPI, se hace así para que la base de datos se prepare justo antes de que el servidor acepte peticiones"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    # El código aquí se ejecuta al INICIAR la app
    create_db_and_tables()
    yield
    # El código aquí se ejecuta al APAGAR la app (si necesitas cerrar conexiones)


app = FastAPI(lifespan=lifespan)
