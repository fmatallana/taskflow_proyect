from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

# 🔵 IMPORTACIONES ABSOLUTAS (app.xxx)
# Cambio de importaciones relativas (from ..db import) a absolutas para evitar circular imports
from app.database import Sessiondep
from app.models.users import User, UserBase, UserCreate
from app.security import (
    crear_token_acceso,
    encriptar_contrasena,
    verificacion_de_contrasena,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, session: Sessiondep):
    hashed_password = encriptar_contrasena(user_data.password)
    user_dict = user_data.model_dump()
    user_dict["hashed_password"] = hashed_password
    user = User.model_validate(user_dict)
    # se crea la funcion fake_hash_password para simular un hasheo de contraseña, luego se crea una variable hashed_password en la que se usa la funcion y se le pasa el parametro password que usa user_data, luego a una variable se le pasa el diccionario user_data.model_dump(), luego a ese diccionario se le agrega la llave hashed_password con su valor hashed_password y a la creacion del user se le pasa la funcion model_validate con el parametro user_dict que fue el diccionario que se creo
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserBase)
async def get_user(user_id: int, session: Sessiondep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"No hay users con el id {user_id}")
    return user


@router.post("/login")
async def user_validate(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Sessiondep = None,
    # Cambiamos a OAuth2PasswordRequestForm para que el endpoint sea compatible
    # con el estándar OAuth2 y el botón 'Authorize' de Swagger.
    # A diferencia de un JSON común, este esquema espera los datos como un
    # formulario (form-data), extrayendo automáticamente 'username' y 'password'.
):
    statement = select(User).where(User.username == form_data.username)
    user_db = session.exec(statement).first()
    if not user_db:
        raise HTTPException(
            status_code=401, detail=f"No hay users con el id {form_data.username}"
        )
    verificar_contraseña = verificacion_de_contrasena(
        form_data.password, user_db.hashed_password
    )
    if not verificar_contraseña:
        raise HTTPException(status_code=401, detail="contraseña incorrecta")
    else:
        token_generado = crear_token_acceso({"sub": user_db.username})
        return {"access_token": token_generado, "token_type": "bearer"}
