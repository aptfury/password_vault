'''
AUTHOR: Blake Lemarr
DATE: 05.09.26
DESCRIPTION: Test cases for storage config
'''

def test_without_subclass(tmp_path, storage_config) -> None:
    config = storage_config
    config.test_db_name = 'account'

    expected_path = tmp_path / 'account.json'

    assert storage_config._database == expected_path