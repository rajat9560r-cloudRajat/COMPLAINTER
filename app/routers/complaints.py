from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix = "/complaints",
    tags = ['complaints']
)


@router.get("/", response_model=List[schemas.Return])
def get_allcomplaints(db:Session = Depends(get_db)):
    all_complaints = db.query(models.Complaint).all()
    if not all_complaints:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="no complaints found")
    return all_complaints

@router.get("/{id}",response_model=schemas.Return)
def get_onecomplaint(id:int, db:Session = Depends(get_db)):
    get_query = db.query(models.Complaint).filter(models.Complaint.id==id)
    one_complaint = get_query.first()
    if not one_complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="complaint with this id was not found")
    return one_complaint

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Return)
def post_complaint(new_data:schemas.Validation, db:Session = Depends(get_db)):
    post_query = models.Complaint(**new_data.model_dump())
    db.add(post_query)
    db.commit()
    db.refresh(post_query)
    return post_query

@router.delete("/{id}" )
def delete_complaint(id:int, db:Session = Depends(get_db)):
    delete_query = db.query(models.Complaint).filter(models.Complaint.id==id)
    todelete = delete_query.first()
    if not todelete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="complaint with this id was not found")
    db.delete(todelete)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{id}",response_model=schemas.Return)
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

@router.put("/{id}",response_model=schemas.Return)
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
