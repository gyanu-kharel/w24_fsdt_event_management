from fastapi import FastAPI, HTTPException
from models import User
from schemas import RegisterUser, AuthResponse, LoginUser
from database import auth_db_collection
from utils import get_password_hash, create_access_token, verify_password

app = FastAPI()



@app.post("/auth/register",
          response_model=AuthResponse,
          response_model_by_alias=False)
async def register(user:RegisterUser):

    if not user.name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    if not user.email:
        raise HTTPException(status_code=400, detail="Email cannot be empty")
    
    if not user.password or len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be atleast 6 digit long")
    
    duplicateEmail = await auth_db_collection.find_one({'email': user.email.lower()})

    if duplicateEmail:
        raise HTTPException(status_code=400, detail="Email already in use")

    hashed_password = get_password_hash(user.password)
    db_user = User(full_name=user.name, email=user.email.lower(), password=hashed_password)
    new_user = await auth_db_collection.insert_one(db_user.model_dump(by_alias=True, exclude=["id"]))

    created_user = await auth_db_collection.find_one({"_id": new_user.inserted_id})

    jwt_data = {
        "id": str(created_user["_id"]),
        "name": created_user['full_name'],
        "email": created_user['email']
    }

    jwt = create_access_token(jwt_data)
    token = AuthResponse(access_token=jwt)
    return token



@app.post('/auth/login', 
          response_model=AuthResponse,
          response_model_by_alias=False)
async def login(request:LoginUser):
    user = await auth_db_collection.find_one({'email': request.email})

    if not user:
        raise HTTPException(status_code=400, detail='Invalid login credentials')

    if not verify_password(request.password, user['password']):
        raise HTTPException(status_code=400, detail='Invalid login credentials')

    jwt_data = {
        "id": str(user["_id"]),
        "name": user['full_name'],
        "email": user['email']
    }

    jwt = create_access_token(jwt_data)
    token = AuthResponse(access_token=jwt)
    return token