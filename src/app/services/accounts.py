# Name: Blake Lemarr
# Updated: 04.01.2026
# Description: Manages account access and data maintenance.

# ===== IMPORTS =====
import json
from ..models import AccountInternal, AccountPublic, AccountStatus, CreateAccount
from ..services import FileManagementService
# ===================

class AccountsService:
    def __init__(self):
        self.service = FileManagementService('vault', 'accounts')
        self.file_path = self.service.construct_path()
        self.valid_path = self.service.create_if_missing()
        self.__load = self.service.read_file
        self.__save = self.service.save_file

    def __fetch_accounts(self) -> list[AccountInternal] | None:
        data = self.__load(self.file_path)
        return [AccountInternal.model_validate(acc) for acc in data]

    def create_new_account(self, new_user: AccountInternal) -> bool | None:
        '''
        Creates a new account and adds it to the database.

        :param new_user:
        :return:
        '''

        if self.valid_path:
            accounts: list[AccountInternal] = self.__fetch_accounts()

            if any(new_user.username.lower() == user.username.lower() for user in accounts):
                print('This username is already in use. Please register again with a different username.')
                return False

            if len(accounts) == 0:
                new_user.status = AccountStatus.ADMIN
                print('As the first user, you have been made the admin of this instance.')

            # add user to data
            accounts.append(new_user)

            # write data
            self.__save(self.file_path, accounts)

            return True
        else:
            return None

    def update_account(self, status: AccountStatus, username: str, update: CreateAccount | AccountInternal) -> bool | None:
        '''
        Allows updating of user accounts. Admins can update various accounts, while users can
        only update their own accounts.

        :param status:
        :param username:
        :param update:
        :return:
        '''

        if status == AccountStatus.BANNED or status == AccountStatus.ON_HOLD:
            print('----- PERMISSION DENIED -----\n'
                  f'You cannot change your account because it is {status}.\n'
                  'If you believe this was an error, please reach out to the administrator.')
            return False # todo - add an access denied response that tells the application to exit

        if self.valid_path:
            accounts: list[AccountInternal] = self.__fetch_accounts()

            if len(accounts) == 0:
                return None

            for i, user in enumerate(accounts):
                if user.username.lower() == username.lower():
                    if status == AccountStatus.ADMIN:
                        accounts[i] = update
                        break

                    elif status == AccountStatus.USER:
                        if update.username:
                            accounts[i].username = update.username

                        if update.email:
                            accounts[i].pii_email = update.email

                        break

                    else:
                        print('ERROR: Only users and admin can edit accounts')
                        return None

            self.__save(self.file_path, accounts)

            return True
        else:
            print('----- INVALID PATH -----')
            return False # todo - create invalid path error

    def find_account_by_username(self, username: str, status: AccountStatus) -> AccountPublic | AccountInternal | None:
        '''
        Finds an account by its username and returns an internal view for admins
        and a public view for users.

        :param username:
        :param status:
        :return:
        '''

        # ensure accounts with restricted access permissions are automatically denied
        if status == AccountStatus.BANNED or status == AccountStatus.ON_HOLD:
            return None # todo - Create access rejection error msg

        if self.valid_path:
            # load data
            accounts: list[AccountInternal] = self.__fetch_accounts()

            if len(accounts) == 0:
                return None

            for user in accounts:
                if username.lower() == user.username.lower():
                    if status == AccountStatus.ADMIN:
                        return user

                    elif status == AccountStatus.USER:
                        return AccountPublic.model_construct(**user.model_dump())

                    else:
                        return None

            return None
        else:
            return None

    def internal_find_all_users(self, status: AccountStatus) -> list[AccountInternal] | None:
        '''
        Returns a list of all registered users.

        :param status:
        :return:
        '''

        if status != AccountStatus.ADMIN:
            return None # todo - replace with access error

        if self.valid_path:
            return self.__fetch_accounts()
        else:
            return None # todo - replace with path error

    # todo - expand based on email and id
    def remove_account_by_username(self, username: str, status: AccountStatus) -> bool | None:
        '''
        Removes an account by its username.

        :param username:
        :param status:
        :return:
        '''

        if status == AccountStatus.BANNED or status == AccountStatus.ON_HOLD:
            return None

        if self.valid_path:
            # load data
            accounts: list[AccountInternal] = self.__fetch_accounts()

            if len(accounts) == 0:
                return None # todo - return an error for no user

            for user in accounts:
                if username.lower() == user.username.lower():
                    accounts.remove(user)

            # save data
            self.__save(self.file_path, accounts)

            return True
        else:
            return False