from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix = "/complaints",
    tags = ['complaints']
)

'''get all'''
@router.get("/", response_model=List[schemas.Return])
def get_allcomplaints(db:Session = Depends(get_db)):
    complaints = db.query(models.Complaint).all()
    if not complaints:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="no complaints found")
    return complaints

'''get by id'''
@router.get("/{id}",response_model=schemas.Return)
def get_onecomplaint(id:int, db:Session = Depends(get_db)):
    complaint = db.query(models.Complaint).filter(models.Complaint.id==id).first()
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="complaint with this id was not found")
    return complaint

'''create complaint'''
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Return)
def post_complaint(new_data:schemas.Validation, db:Session = Depends(get_db)):
    complaint = models.Complaint(**new_data.model_dump())
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint

'''delete complaint by id'''
@router.delete("/{id}" )
def delete_complaint(id:int, db:Session = Depends(get_db)):
    complaint = db.query(models.Complaint).filter(models.Complaint.id==id).first()
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="complaint with this id was not found")
    db.delete(complaint)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

'''update some fields'''
@router.patch("/{id}",response_model=schemas.Return)
def update_complaint(new_data:schemas.Postupdate, id:int, db:Session = Depends(get_db) ):
    complaint = db.query(models.Complaint).filter(models.Complaint.id == id).first()
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="complaint with this id was not found")
    updated_details = new_data.model_dump(exclude_unset=True)
    for key, value in updated_details.items():
        setattr(complaint, key, value)
    db.commit()
    db.refresh(complaint)
    return complaint

'''replace all input fields'''
@router.put("/{id}",response_model=schemas.Return)
def replace_complaint(data:schemas.PostReplace, id:int, db:Session = Depends(get_db) ):
    complaint = db.query(models.Complaint).filter(models.Complaint.id == id).first()
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="complaint with this id was not found")
    replacing_details = data.model_dump(exclude_unset=True)
    for key, value in replacing_details.items():
        setattr(complaint, key, value)
    db.commit()
    db.refresh(complaint)
    return complaint
