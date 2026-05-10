'''
AUTHOR: Blake Lemarr
DATE: 05.09.26
DESCRIPTION: Test cases for storage config
'''

from app.storage import StorageConfig

def test_without_subclass(tmp_path, storage_config) -> None:
    config_kwargs = {
        'is_test': True,
        'test_dir': tmp_path,
        'test_db_name': 'accounts'
    }

    storage: StorageConfig = StorageConfig(**config_kwargs)
    storage.database

    # Mimic the current path we set up in conftest
    expected_path = tmp_path / 'accounts.json' # < the db_name/test_db_name ingested by the storage
                                          # config should stay without the file extension
    storage._test_only()
    assert storage.database == expected_path