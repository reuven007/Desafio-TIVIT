
import requests
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..repositories.database import get_db
from ..model.models import UserData 
from datetime import datetime, timedelta



# log de informação
log = logging.getlog("rich")

router = APIRouter()

SECRET_KEY = "4b340366f20f5e2f9325f4e6ebf05f65ed346e7afbecc4d6f308255c5e26e36f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 40


FAKE_API_BASE_URL = "https://api-onecloud.multicloud.tivit.com/fake"

# Configura o esquema de segurança OAuth2 com "Bearer Token"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "user": {"username": "user", "role": "user", "password": "L0XuwPOdS5U"},
    "admin": {"username": "admin", "role": "admin", "password": "JKSipm0YH"},
}


# Decodifica e valida o token JWT para obter o usuário atual
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        password: str = payload.get("password") 
        if username is None or role is None or password is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"username": username, "role": role, "password": password}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        


# Obtém um token falso para autenticação com o serviço externo
def get_fake_service_token(username, password):
    log.info("Iniciando a autenticação com o serviço externo.")
    log.debug(f"Parâmetros recebidos - username: {username}")

    params = {
        "username": username,
        "password": password
    }
    response = requests.post(
        f"{FAKE_API_BASE_URL}/token",
        params=params, 
        verify=False 
    )
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise HTTPException(status_code=401, detail="Unable to authenticate with external service")


# Salva dados recuperados de um serviço externo no banco de dados local
def save_fake_data(db: Session, username: str, role: str, data: dict):
    user_data = UserData(username=username, role=role, data=data)
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data

# Verifica se a senha fornecida corresponde à senha armazenada
def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password


# Cria um token de acesso JWT com dados do usuário e tempo de expiração
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
