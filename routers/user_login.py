from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from routers import token
from database import database, models, schemas

router = APIRouter(tags=['user_login'], prefix='/login')


@router.post('')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.Student).filter(models.Student.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User Not Found")

    if not (user.password == request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password")
    access_token = token.create_access_token(data={"sub": user.name, "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


