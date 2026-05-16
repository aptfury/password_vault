'''
AUTHOR: Blake Lemarr
DATE: 05.14.26
DESCRIPTION: Test cases for vault repo
'''

import json
import pytest

from datetime import datetime
from pathlib import Path

from app.models import AccountAuthModel, AccountModel, VaultModel, VaultEntryModel, VaultLoginDataModel

from app.repositories import VaultRepo

def test_vault_repo_create_vault(tmp_path, vault_repo, account_factory, vault_entry_factory, auth_service):
    #### PATH CONFIGS ####
    test_dir: Path = tmp_path / 'database'
    test_dir.mkdir(parents=True, exist_ok=True)
    vaults_path: Path = test_dir / 'vaults.json'
    accounts_path: Path = test_dir / 'accounts.json'
    
    with open(vaults_path, 'w', encoding='utf-8') as file:
        json.dump([], file, indent=4)
        
    with open(accounts_path, 'w', encoding='utf-8') as file:
        json.dump([], file, indent=4)
    ######################
        
    # CREATE USER #
    user, raw_password = account_factory()
    
    assert isinstance(user, AccountModel)
    ###############
    
    # BUILDER USER VAULT #
    vault: VaultModel = VaultModel(
        _id=user.password.vault_id,
        user_id=user.id,
        created=str(datetime.now()),
        vault=[]
    )
    ######################
    
    # CONNECT & CREATE #
    auth_service.login(name=user.name, raw_password=raw_password)
    repo: VaultRepo = vault_repo(vault_id=user.password.vault_id, session=auth_service.encrypt_utils._fernet)
    
    created: bool = repo.create(data=vault)
    
    assert created
    ####################
    
    # FIND VAULT AND VALIDATE #
    raw_data: list = []
    
    with open(vaults_path, 'r', encoding='utf-8') as file:
        raw_data = json.load(file)
        
    vaults: list = [VaultModel.model_validate(v) for v in raw_data]
    
    assert vault in vaults
    ###########################
    
    # GET ALL #
    vaults = repo.get_all()
    assert vault in vaults
    ###########
    
    # GET VAULT ID #
    v_id: str = repo.get_id('user_id', user.id)
    assert v_id == vault.id
    ################
    
    # GET VAULT BY ID #
    v_by_id: VaultModel = repo.get_by_id(vault.id)
    assert v_by_id == vault
    ###################
    
    # GET ONE WHERE #
    v_by_where: VaultModel = repo.get_one_where('user_id', user.id)
    assert v_by_where == vault
    #################
    
    # GET ALL WHERE #
    auth_service.logout()
    user_two, raw_password_two = account_factory()
    auth_service.login(name=user_two.name, raw_password=raw_password_two)
    
    vault_two: VaultModel = VaultModel(
        _id=user_two.password.vault_id,
        user_id=user_two.id,
        created=str(datetime.now()),
        vault=[]
    )
    
    repo_two: VaultRepo = vault_repo(vault_id=user_two.password.vault_id, session=auth_service.encrypt_utils._fernet)
    
    created_two = repo_two.create(vault_two)
    
    assert created_two
    
    v_all_by_where: list[VaultModel] = repo_two.get_all_where(key='vault', value=[])
    
    assert vault in v_all_by_where
    assert vault_two in v_all_by_where
    #################
    
    # UPDATE ONE WHERE #
    v_by_id: VaultModel = repo_two.get_by_id(vault_two.id)
    v_entry = vault_entry_factory()
    v_by_id.vault.append(v_entry)
    repo_two.update_one_where(data=v_by_id, key='_id', value=v_by_id.id)
    vault_two_entries: VaultModel = repo_two.get_one_where(key='_id', value=v_by_id.id)
    
    assert v_entry in vault_two_entries.vault
    auth_service.logout()
    ####################
    
    # DELETE ONE WHERE & DELETE ALL WHERE #
    user_three, raw_password = account_factory()
    auth_service.login(user_three.name, raw_password)
    repo_three: VaultRepo = vault_repo(vault_id=user_three.password.vault_id, session=auth_service.encrypt_utils._fernet)
    vault_entry_three = vault_entry_factory()
    vault_three: VaultModel = VaultModel(
        _id=user_three.password.vault_id,
        user_id=user_three.id,
        created=str(datetime.now()),
        vault=[vault_entry_three]
    )
    repo_three.create(vault_three)
    get_v3 = repo_three.get_by_id(vault_three.id)
    assert get_v3 == vault_three
    
    deleted: bool = repo.delete_one_where(key='user_id', value=user.id)
    
    assert deleted
    
    vault.user_id = user_three.id
    repo_three.create(vault)
    
    v_all: list = repo_three.get_all()
    assert len(v_all) == 3
    
    all_deleted = repo_three.delete_all_where('user_id', user_three.id)
    
    v_all: list = repo_three.get_all()
    vault_of_user_two: VaultModel = repo_three.get_one_where('user_id', user_two.id)
    
    assert all_deleted
    assert len(v_all) == 1
    assert vault_of_user_two.id == vault_two.id
    ######################################
    
    # DELETE FILE #
    database_deleted = repo_three.delete_database()
    
    assert database_deleted
    assert test_dir.exists()
    assert accounts_path.exists()
    assert not vaults_path.exists()
    ###############