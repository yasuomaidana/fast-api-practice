from pydantic import BaseModel, EmailStr

from models import Account


class CreateUserDto(BaseModel):
    username: str
    password: str
    email: EmailStr
    
    def to_account(self) -> Account:
        return Account(username=self.username, email=self.email, password=self.password)
