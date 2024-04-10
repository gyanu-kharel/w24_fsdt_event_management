from fastapi import FastAPI, HTTPException
from models import User
from schemas import RegisterUser, AuthResponse
from database import auth_db_collection
from utils import hash_password, create_access_token

app = FastAPI()



@app.post("/auth/register",
          response_model=AuthResponse,
          response_model_by_alias=False)
async def create_user(user:RegisterUser):

    if not user.name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    if not user.email:
        raise HTTPException(status_code=400, detail="Email cannot be empty")
    
    if not user.password or len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be atleast 6 digit long")
    
    duplicateEmail = auth_db_collection.find({'email': user.email.lower()})

    if duplicateEmail:
        raise HTTPException(status_code=400, detail="Email already in use")

    hashed_password = hash_password(user.password)
    db_user = User(full_name=user.name, email=user.email.lower(), password=hashed_password)
    new_user = await auth_db_collection.insert_one(db_user.model_dump(by_alias=True, exclude=["id"]))

    created_user = await auth_db_collection.find_one({"_id": new_user.inserted_id})

    print(created_user)

    jwt_data = {
        "id": str(created_user["_id"]),
        "name": created_user['full_name'],
        "email": created_user['email']
    }

    jwt = create_access_token(jwt_data)
    token = AuthResponse(access_token=jwt)
    return token