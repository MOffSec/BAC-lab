from fastapi import FastAPI, Depends, Body, status, Response
from fastapi.responses import JSONResponse
from Models.user import User, SessionLocal
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

app = FastAPI()


# Dependency function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Define the user registration request body schema
class UserRegister(BaseModel):
    username: str
    password: str
    role: Optional[str]


class LogIn(BaseModel):
    username: str
    password: str


@app.get("/")
async def home():
    return JSONResponse(content={"status": "success"})


@app.get("/admin/dashboard/{user_id}")
async def admin(user_id: int, db: Session = Depends(get_db)):
    # Check if user exists with the given user_id (assuming id is used for authentication)
    user = db.query(User).filter(User.id == user_id).first()
    if user.role == "admin":
        return JSONResponse(content={"status": "success", "message": "Harri OMH!"})
    else:
        return Response(content={"message": "Unauthorized"}, status_code=status.HTTP_401_UNAUTHORIZED)


# User registration endpoint
@app.post("/register")
async def register_user(user: UserRegister = Body(...), db=Depends(get_db)):
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        return {"message": "Username already exists"}

    # Create a new user object
    new_user = User(username=user.username, password=user.password, role=user.role)

    # Add the new user to the database
    db.add(new_user)
    db.commit()

    return {"message": f"User registered successfully: {user.username}"}


@app.post("/login")
async def login(cred: LogIn = Body(...), db: Session = Depends(get_db)):
    username = cred.username
    password = cred.password
    user = db.query(User).filter(User.username == username, User.password == password).first()
    if user:
        # Check for user role
        if user.role == "admin":
            # Redirect to admin dashboard
            admin_url = f"/admin/dashboard/{user.id}"
            response = Response()
            response.headers["Location"] = admin_url
            response.status_code = status.HTTP_302_FOUND
            return response
        else:
            # Return success message for valid login (non-user roles)
            return JSONResponse(content={"status": "success", "message": "Login successful", "role": f"{user.role}"})
    else:
        # Login failed (invalid credentials)
        return JSONResponse(content={"status": "error", "message": "Invalid username or password"})

