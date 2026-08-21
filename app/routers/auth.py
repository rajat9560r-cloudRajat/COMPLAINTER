from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from .. import models, schemas, utils
from ..database import  get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags = ['authentication'] #tags sirf or sirf swagger ui ke liye hai 
)

@router.post("/login")
def user_login(data:schemas.Credentials, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==data.email).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="invalid credintials")
    if not utils.hashverify(data.password, user.password):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="invalid credintials")
    return {"happy happy happy"}