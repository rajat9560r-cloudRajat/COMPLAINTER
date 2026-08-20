from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from .. import models, schemas, utils
from ..database import  get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix = "/users",
    tags = ['users']
)




@router.get("/", response_model=List[schemas.ResponseReturn])
def get_all_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="no registered users")
    return users

@router.get("/{id}", response_model=schemas.ResponseReturn)
def get_by_id(id:int, db:Session=Depends(get_db)):
    get_query=db.query(models.User).filter(models.User.id==id)
    user=get_query.first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user not found with this id")
    return user

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.ResponseReturn)
def create_user(data:schemas.NewUser, db:Session=Depends(get_db)):

    hashed_pass = utils.hashpass(data.password)
    data.password = hashed_pass

    new_user = models.User(**data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete("/{id}", response_model=schemas.ResponseReturn )
def delete_user(id:int, db:Session=Depends(get_db)):
    delete_query=db.query(models.User).filter(models.User.id==id)
    user = delete_query.first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user with this id not present")
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{id}", response_model=schemas.ResponseReturn )
def delete_user(data:schemas.UserUpdate,id:int, db:Session=Depends(get_db)):
    update_query=db.query(models.User).filter(models.User.id==id)
    user = update_query.first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user with this id not present")
    update_query.update(data.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(user)
    return user

@router.put("/{id}", response_model=schemas.ResponseReturn )
def delete_user(data:schemas.UserReplace,id:int, db:Session=Depends(get_db)):
    replace_query=db.query(models.User).filter(models.User.id==id)
    user = replace_query.first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user with this id not present")
    replace_query.update(data.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(user)
    return user
