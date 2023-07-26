from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import  CryptContext
from sqlalchemy.orm import Session
from  database import engine, SessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = 'secret'
ALGORITHM = 'HS256'



class  createUser(BaseModel):
  username : str
  email : Optional[str] = None
  first_name : Optional[str]
  last_name : Optional[str]
  password : str

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

models.Base.metadata.create_all(bind=engine)

OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

app = FastAPI()

def get_password_hash(password):
  return bcrypt_context.hash(password)

def verify_password(plain_password, hashed_password):
  return bcrypt_context.verify(plain_password, hashed_password)

def create_access_token(username: str, user_id:int, expires_delta: Optional[timedelta] = None):
     encode_data = {"sub": username, "user_id": user_id}
     if expires_delta:
        expire = datetime.utcnow() + expires_delta
     else:
        expire = datetime.utcnow() + timedelta(minutes=15)
     encode_data.update({"exp": expire})
     return jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(OAuth2PasswordBearer), db:Session=Depends(get_db)):
     try:
        payload =jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if username is None:
            raise HTTPException(status_code=401, detail="user not found")
        return {"username":username ,"id":user_id }
     except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Credentials")


def authenticate_user(username:str, password:str, db:Session=Depends(get_db)):
     user=db.query(models.Users).filter(models.Users.username==username).first()
     if not user:
        return False
     if not verify_password(password, user.hashed_password):
         return False
     return user

@app.post("/create/user")
async def create_user(create_user: createUser, db: Session = Depends(get_db)):
     create_user= models.Users(username=create_user.username, email=create_user.email, first_name=create_user.first_name, last_name=create_user.last_name, hashed_password=get_password_hash(create_user.password), is_active=True)
     db.add(create_user)
     db.commit()
     db.refresh(create_user)
     return {"message": "User Created"}


@app.post("/token")

async def login_for_access_token(form_data:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
  user = authenticate_user(form_data.username, form_data.password, db)
  if not user:
     raise HTTPException(status_code=401, detail="Invalid Credentials")
  token_expires = timedelta(minutes=15)
  token =create_access_token (user.username, user.id, expires_delta=token_expires)

  return {
    "access_token": token,
    "token_type": "bearer"
  }
