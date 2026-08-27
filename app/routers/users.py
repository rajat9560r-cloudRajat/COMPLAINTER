from fastapi import Depends, HTTPException, status, Response, APIRouter
from .. import models, schemas, utils
from ..database import  get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix = "/users",
    tags = ['users']
)

'''get all users'''
@router.get("/", response_model=List[schemas.ResponseReturn])
def get_all_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No registered users")
    return users

'''get user by id'''
@router.get("/{id}", response_model=schemas.ResponseReturn)
def get_by_id(id:int, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found with this id")
    return user

'''create new user'''
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.ResponseReturn)
def create_user(data:schemas.NewUser, db:Session=Depends(get_db)):

    hashed_pass = utils.hashpass(data.password)
    data.password = hashed_pass

    new_user = models.User(**data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

'''delete user by id'''
@router.delete("/{id}")
def delete_user(id:int, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User with this id not present")
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

'''update some fields'''
@router.patch("/{id}", response_model=schemas.ResponseReturn )
def update_user(data:schemas.UserUpdate,id:int, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User with this id not present")
    updated_details = data.model_dump(exclude_unset=True)

    if "password" in updated_details:
        updated_details["password"] = utils.hashpass(updated_details["password"])

    for key, value in updated_details.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

'''replace all input fields'''
@router.put("/{id}", response_model=schemas.ResponseReturn )
def replace_user(data:schemas.UserReplace,id:int, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User with this id not present")
    replacing_details = data.model_dump(exclude_unset=True)

    if "password" in replacing_details:
        replacing_details["password"] = utils.hashpass(replacing_details["password"])

    for key, value in replacing_details.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
