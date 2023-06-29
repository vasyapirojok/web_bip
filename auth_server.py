from datetime import datetime, timedelta
from mail_sender import send

from random import choice as rch
import uvicorn
import random
import string
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.responses import FileResponse, Response, RedirectResponse, JSONResponse
from fastapi.requests import Request
from db import DB

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "$2b$12$1YmmNxgdSJOTKofNwQ3NOuZJpa9l48OhkFGOm1Iok5xqBLzVPs.Vm",
        "disabled": False,
    }
}

db = DB()

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    username: str
    email: str = None
    disabled: bool = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def generate_auth_code():
    code = ''
    for _ in range(6):
        code += f'{rch(range(0, 9))}'
    return '000000'
    return code


def get_user(username: str):
    user_dict = db.get_user(username)
    if user_dict is not None:
        return UserInDB(**user_dict)


def authenticate_user(username: str):
    user = get_user(username)
    if not user:
        return False
    # if not verify_password(password, user.hashed_password):
    #     return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def generate_salt(length: int):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    # if token_data["exp"] > 
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(email: str):
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

@app.get("/signup_salt")
async def signup_salt(email: str):
    salt = generate_salt(32)
    if not db.check_email_exists(email):
        db.add_user(email, salt)
        return JSONResponse(content={"salt": salt, "available": 1})
    return JSONResponse(content={"salt": salt, "available": 0})

@app.post("/signup_creds")
async def check_creds(email: str, password: str):
    db.set_password(email, password)
    code = generate_auth_code()
    db.set_code(email, code)
    send(email, code)
    return JSONResponse()


@app.post("/check_code")
async def check_creds(email: str, code: str):
    if db.check_code(email, code):
        return JSONResponse(content={"status": "OK"})
    return JSONResponse(content={"status": "ERROR"})



@app.get("/login_salt")
async def login_salt(email: str):
    salt = db.get_salt(email)
    print("SALT:       ", salt)
    if db.check_email_exists(email):
        return JSONResponse(content={"salt": salt, "available": 1})
    return JSONResponse(content={"salt": salt, "available": 0})

@app.post("/login_creds")
async def check_creds(email: str, password: str):
    
    if db.check_creds(email, password):
        code = generate_auth_code()
        db.set_code(email, code)
        send(email, code)
        return JSONResponse(content={"status": "OK"})
    else:
        return JSONResponse(content={"status": "ERROR"})


@app.post("/check_csrf")
async def check_csrf(email: str, csrf: str):
    if db.check_csrf(email, csrf):
        return JSONResponse(content={"status": "OK"})
    else:
        return JSONResponse(content={"status": "ERROR"})

@app.post("/set_csrf")
async def set_csrf(email: str, csrf: str):
    db.set_csrf(email, csrf)


uvicorn.run(app, port=8002)