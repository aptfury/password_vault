# Name: Blake Lemarr
# Updated: 04.01.2026
# Description: Manages logic for account handling.

# ===== IMPORTS =====
import os
from .auth_util import AuthUtilities
from enum import Enum
from dotenv import load_dotenv
from ..models import (
    AccountPublic,
    AccountInternal,
    CreateAccount,
    AccountPassword,
    AccountStatus
)
from ..services import AccountService, StorageService

# ===== UTILITIES =====

load_dotenv()
account_storage: StorageService = StorageService('data', 'accounts.json')

class AcceptedFields(str, Enum):
    id = 'id'
    username = 'username',
    pii_email = 'pii_email',
    email = 'pii_email',
    created_on = 'created_on',
    status = 'status'

class AccountUtil:
    def __init__(self):
        self.service = AccountService(storage=account_storage)
        self.fields = AcceptedFields
        self.__auth = AuthUtilities()
        self.__pepper = os.getenv("ACCOUNT_PEPPER")

    def __action_forbidden(self, status: AccountStatus, admin_only: bool = False) -> bool:
        '''Checks if the action taken is forbidden based on permissions.'''
        if status == AccountStatus.ADMIN:
            return False

        if admin_only:
            return True

        if status == AccountStatus.USER:
            return False

        return True

    def __is_admin(self, status: AccountStatus) -> bool:
        '''Shorthand to check if the user is an admin.'''
        if status == AccountStatus.ADMIN:
            return True

        return False

    def __is_self_query(
            self,
            user: AccountInternal,
            field: str | None = None,
            search: str | None = None,
            target: AccountInternal | None = None
    ) -> bool:
        '''Checks if the user is querying their own account'''
        if target is not None:
            if user.id == target.id:
                return True

        if field is not None and search is not None:
            if getattr(user, field).lower() == search.lower():
                return True

        return False

    def create(self, data: CreateAccount) -> bool:
        '''
        Creates a new account for the user.

        :param data:
        :return:
        '''

        # hash user password
        hashed_password: AccountPassword = self.__auth.new_account_password(data.password)

        # create account model
        new_account: AccountInternal = AccountInternal(
            username=data.username,
            pii_email=data.email,
            hashed_password=hashed_password
        )

        # create new account
        return self.service.create(new_account)

    # def query_user(
    #         self,
    #         user: AccountInternal,
    #         fields: AcceptedFields,
    #         search: str | AccountStatus
    # ) -> AccountInternal | AccountPublic | None:
    #