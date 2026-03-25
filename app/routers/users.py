from fastapi import APIRouter, HTTPException, status

from app.database import Sessiondep
from app.models.users import User, UserBase, UserCreate

router = APIRouter(prefix="/users", tags=["Users"])


def fake_hash_password(password: str) -> str:
    return f"super_secret_{password}"


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, session: Sessiondep):
    hashed_password = fake_hash_password(user_data.password)
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
