from fastapi import FastAPI, Depends, HTTPException, status, Response
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import Optional, List

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/complaints", response_model=List[schemas.Return])
def get_allcomplaints(db:Session = Depends(get_db)):
    all_complaints = db.query(models.Complaint).all()
    if not all_complaints:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="no complaints found")
    return all_complaints

@app.get("/complaints/{id}",response_model=schemas.Return)
def get_onecomplaint(id:int, db:Session = Depends(get_db)):
    get_query = db.query(models.Complaint).filter(models.Complaint.id==id)
    one_complaint = get_query.first()
    if not one_complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="complaint with this id was not found")
    return one_complaint

@app.post("/complaints",status_code=status.HTTP_201_CREATED, response_model=schemas.Return)
def post_complaint(new_data:schemas.Validation, db:Session = Depends(get_db)):
    post_query = models.Complaint(**new_data.model_dump())
    db.add(post_query)
    db.commit()
    db.refresh(post_query)
    return post_query

@app.delete("/complaints/{id}" )
def delete_complaint(id:int, db:Session = Depends(get_db)):
    delete_query = db.query(models.Complaint).filter(models.Complaint.id==id)
    todelete = delete_query.first()
    if not todelete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="complaint with this id was not found")
    db.delete(todelete)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.patch("/complaints/{id}",response_model=schemas.Return)
def update_complaint(new_data:schemas.Postupdate, id:int, db:Session = Depends(get_db) ):
    update_query = db.query(models.Complaint).filter(models.Complaint.id == id)
    toupdate=update_query.first()
    if not toupdate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="complaint with this id was not found")
    update_query.update(new_data.model_dump(exclude_unset=True),synchronize_session=False)
    db.commit()
    db.refresh(toupdate)
    return toupdate

@app.put("/complaints/{id}",response_model=schemas.Return)
def replace_complaint(data:schemas.PostReplace, id:int, db:Session = Depends(get_db) ):
    replace_query = db.query(models.Complaint).filter(models.Complaint.id == id)
    toreplace=replace_query.first()
    if not toreplace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="complaint with this id was not found")
    replace_query.update(data.model_dump(exclude_unset=True),synchronize_session=False)
    db.commit()
    db.refresh(toreplace)
    return toreplace

'''users design '''
'''new routes, new table, all new'''

@app.get("/users", response_model=List[schemas.ResponseReturn])
def get_all_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="no registered users")
    return users

@app.get("/users/{id}", response_model=schemas.ResponseReturn)
def get_by_id(id:int, db:Session=Depends(get_db)):
    get_query=db.query(models.User).filter(models.User.id==id)
    user=get_query.first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user not found with this id")
    return user

@app.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.ResponseReturn)
def create_user(data:schemas.NewUser, db:Session=Depends(get_db)):
    new_user = models.User(**data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.delete("/users/{id}", response_model=schemas.ResponseReturn )
def delete_user(id:int, db:Session=Depends(get_db)):
    delete_query=db.query(models.User).filter(models.User.id==id)
    user = delete_query.first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user with this id not present")
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.patch("/users/{id}", response_model=schemas.ResponseReturn )
def delete_user(data:schemas.UserUpdate,id:int, db:Session=Depends(get_db)):
    update_query=db.query(models.User).filter(models.User.id==id)
    user = update_query.first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user with this id not present")
    update_query.update(data.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(user)
    return user

@app.put("/users/{id}", response_model=schemas.ResponseReturn )
def delete_user(data:schemas.UserReplace,id:int, db:Session=Depends(get_db)):
    replace_query=db.query(models.User).filter(models.User.id==id)
    user = replace_query.first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user with this id not present")
    replace_query.update(data.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(user)
    return user






