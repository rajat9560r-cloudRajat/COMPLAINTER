from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from .. import models, schemas, utils, oauth2
from ..database import  get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    tags = ['authentication'] #tags sirf or sirf swagger ui ke liye hai 
)

@router.post("/login")
def user_login(data:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==data.username).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="invalid credintials")
    if not utils.hashverify(data.password, user.password):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="invalid credintials")

    token = oauth2.create_access_token({"id":user.id})
    
    return {"access token":token, "type":"bearer"}