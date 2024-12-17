import requests
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..repositories.database import get_db
from ..model.models import UserData 
from ..services.users_services import get_current_user, save_fake_data, get_fake_service_token, create_access_token, verify_password

# log de informação
log = logging.getlog("rich")

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 40


FAKE_API_BASE_URL = "https://api-onecloud.multicloud.tivit.com/fake"

fake_users_db = {
    "user": {"username": "user", "role": "user", "password": "L0XuwPOdS5U"},
    "admin": {"username": "admin", "role": "admin", "password": "JKSipm0YH"},
}


# Endpoint para autenticar usuários e retornar um token de acesso
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict or not verify_password(form_data.password, user_dict["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_dict["username"], "role": user_dict["role"], "password": user_dict["password"]}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



# Retorna dados do usuário autenticado, buscando informações de um serviço externo
@router.get("/user")
async def read_user_data(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "user":
        raise HTTPException(status_code=403, detail="Operation not permitted")
    
    fake_service_token = get_fake_service_token(current_user["username"], current_user["password"])
    headers = {"Authorization": f"Bearer {fake_service_token}"}
    response = requests.get(f"{FAKE_API_BASE_URL}/user", headers=headers, verify=False)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from external service")
    
    save_fake_data(db, current_user["username"], current_user["role"], response.json())
    
    return response.json()


# Retorna dados administrativos, validando se o usuário tem o papel de adm
@router.get("/admin")
async def read_admin_data(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Operation not permitted")

    fake_service_token = get_fake_service_token(current_user["username"], current_user["password"])
    headers = {"Authorization": f"Bearer {fake_service_token}"}
    response = requests.get(f"{FAKE_API_BASE_URL}/admin", headers=headers, verify=False)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from external service")
    
    save_fake_data(db, current_user["username"], current_user["role"], response.json())
    
    return response.json()


# Obtém dados locais armazenados no banco
@router.get("/local_data")
async def get_local_data(db: Session = Depends(get_db)):
    data = db.query(UserData).all()
    return data




    
