from pydantic import BaseModel, EmailStr
from typing import Optional

#class to validate user's input
class Validation(BaseModel):
    name:str
    title:str
    content:str

#complaints - PATCH
class Postupdate(BaseModel):
    name:Optional[str] = None
    title:Optional[str]= None
    content:Optional[str]=None
    status : str | None = None

#complaints - RETURN
class Return(BaseModel):
    id : int
    status : str
    title : str

    class Config:
        orm_mode=True

#complaints - PUT
class PostReplace(BaseModel):
    name:str 
    title:str
    content:str
    status : str

#############################################################################################

'''
3 schemas will be created--> for validation, for update, for returning'''

#user input details verification
class NewUser(BaseModel):
    name : str
    email : EmailStr
    password : str

class UserUpdate(BaseModel):
    name : str | None = None
    email : EmailStr| None = None
    password : str| None = None

class ResponseReturn(BaseModel):
    id : int
    name : str
    email : str
    class Config():
        from_attributes=True 
        #old name was- orm_mode


class UserReplace(BaseModel):
    name:str
    email:EmailStr
    password:str

############################################################################################

class TokenData(BaseModel):
    id : str

class Token(BaseModel):
    access_token : str
    type : str