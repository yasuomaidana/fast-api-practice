from auth import AuthHandler
from dto.user.create_user_dto import CreateUserDto
from repository.account_repository import AccountRepository
from settings import engine


class UserService:
    _instance = None
    auth_handler: AuthHandler
    account_repository = AccountRepository

    def __new__(cls, auth_handler: AuthHandler = AuthHandler(),
                account_repository: AccountRepository = AccountRepository(_engine=engine)):
        if cls._instance is None:
            cls._instance = super(UserService, cls).__new__(cls)
            cls._instance.auth_handler = auth_handler
            cls._instance.account_repository = account_repository

        return cls._instance

    def find_account(self, username: str):
        return self.auth_handler.find_account(username)
    
    def register(self, create_user_dto:CreateUserDto):
        create_user_dto.password = self.auth_handler.get_password_hash(create_user_dto.password)
        return self.account_repository.create(create_user_dto.to_account())
    
    
