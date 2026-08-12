from fastapi import FastAPI, Depends, HTTPException, status, Response

from pydantic import BaseModel
from . import models
from .database import engine, get_db
from sqlalchemy.orm import session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

#class to validate user's input
class Validation(BaseModel):
    name:str
    title:str
    content:str
    
    
#basic working route
@app.get("/")
def root1():
    return {"message":"working fine"}

@app.get("/sqlalchemy")
def root2(db:session = Depends(get_db)):
    return {"message":"first step"}

@app.get("/allcomplaints")
def get_allcomplaints(db:session = Depends(get_db)):
    all_complaints = db.query(models.Complaint).all()
    if not all_complaints:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="no complaints found")
    return {"data":all_complaints}

@app.get("/allcomplaints/{id}")
def get_onecomplaint(id:int, db:session = Depends(get_db)):
    get_query = db.query(models.Complaint).filter(models.Complaint.id==id)
    one_complaint = get_query.first()
    if not one_complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="complaint with this id was not found")
    return {"data":one_complaint}

@app.post("/createcomplaint",status_code=status.HTTP_201_CREATED)
def post_complaint(new_data:Validation, db:session = Depends(get_db)):
    post_query = models.Complaint(**new_data.model_dump())
    db.add(post_query)
    db.commit()
    db.refresh(post_query)
    return {"data":post_query}

@app.delete("/deletecomplaint/{id}")
def delete_complaint(id:int, db:session = Depends(get_db)):
    delete_query = db.query(models.Complaint).filter(models.Complaint.id==id)
    todelete = delete_query.first()
    if not todelete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="complaint with this id was not found")
    db.delete(todelete)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.patch("/updatecomplaint/{id}")
def update_complaint(new_data:Validation, id:int, db:session = Depends(get_db) ):
    update_query = db.query(models.Complaint).filter(models.Complaint.id==id)
    toupdate=update_query.first()
    if not toupdate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="complaint with this id was not found")
    update_query.update(new_data.model_dump(exclude_unset=True),synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_202_ACCEPTED)