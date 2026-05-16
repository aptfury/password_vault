'''
AUTHOR: Blake Lemarr
DATE: 05.09.26
DESCRIPTION: A base class for a storage-based decorator.
'''

# ------------ imports ------------ #
import json
from pathlib import Path

# ------------ storage_config ------------ #
class StorageConfig:
    def __init__(self, db_name: str, db_dir: str = 'database'):
        self.db_name: str = db_name
        self.db_dir: str = db_dir
        self.path: Path = self._build_path()
        
    def _build_path(self) -> Path:
        is_valid: bool = self.validate_data('db_name', self.db_name)
        
        try:
            if is_valid:
                src_dir: Path = Path(__file__).resolve().parent
                db_dir: Path = src_dir / self.db_dir

                db_dir.mkdir(parents=True, exist_ok=True)
                
                db_file: Path = db_dir / f'{self.db_name}.json'
                
                return db_file
            
            else:
                raise FileNotFoundError(f'Could not find {self.db_name}.json')
            
        except Exception as e:
            print(e)
        
    def validate_data(self, key: str, value: str) -> bool:
        try:
            valid_data_set: dict = {
                'action': [
                    'test',
                    'read',
                    'add',
                    'update',
                    'delete'
                ],
                'db_name': [
                    'test',
                    'accounts',
                    'vaults'
                ]
            }
            
            return value in valid_data_set[key]
        
        except Exception as e:
            print(e)
            
    def read(self) -> list[dict]:
        with open(self.path, 'r', encoding='utf-8') as file:
            # todo = create log
            return json.load(file)
        
    def add(self, data: dict) -> bool:
        file: list[dict] = self.read()
        
        file.append(data)
        
        written: bool = self.write_file(file)
        
        file = None
        file = self.read()
        return written and data in file
    
    def update(self, key: str, value: str, data: dict) -> bool:
        file: list[dict] = self.read()
        target: dict = None
        
        for item in file:
            if item[key] == value:
                target = item
                break

        file.remove(target)
        file.append(data)
        
        written: bool = self.write_file(file)
        
        file = None
        file = self.read()
        
        return written and data in file
    
    def delete(self, key: str, value: str) -> bool:
        file: list[dict] = self.read()
        target: dict = None

        for item in file:
            if item[key] == value:
                target = item
                break
            
        file.remove(target)
        
        written = self.write_file(file)
        
        file = None
        file = self.read()
        
        return written and target not in file
        
    def write_file(self, data: list[dict]) -> bool:
        with open(self.path, 'w', encoding='utf-8') as file:
            # todo - turn into log
            json.dump(data, file, indent=4)
            
        return data == self.read()