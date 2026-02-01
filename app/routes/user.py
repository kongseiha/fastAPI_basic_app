from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app.database import engine
from app.model import User  

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User)
def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@router.get("/", response_model=list[User])
def read_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.name = updated_user.name
        user.age = updated_user.age
        user.phone = updated_user.phone
        user.email = updated_user.email
        
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@router.delete("/{user_id}")
def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        session.delete(user)
        session.commit()
        return {"detail": "User deleted successfully"}