'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: Database file that manages File I/O
'''

# ------------ imports ------------ #
import json
from pathlib import Path

# ------------ class ------------ #
class Database:
    def __init__(self, db_path: Path):
        """This class serves as the gateway for all database operations.
        It currently handles File I/O with plans to expand later.

        Args:
            path (Path): The path injected into and accessed by the database
        """        
        self.db_path = db_path
        
    def initialized(self) -> bool:
        """Runs an initialization routine to ensure that the parent
        directory and the file both exist. Populates the file with an empty
        list to avoid json errors.

        Returns:
            bool: if the file exists
        """                
        try:
            if not self.db_path.parent.exists():
                self.db_path.mkdir(parents=True, exist_ok=True)
            
            if not self.db_path.exists():
                self.db_path.touch(exist_ok=True)
                
                # populate path to ensure it's not empty
                with open(self.db_path, 'w', encoding='utf-8') as file:
                    json.dump([], file, indent=4)
                    
            initialized: bool = self.db_path.parent.exists() and self.db_path.exists()   
             
            if initialized:
                print('--------------------------------')
                print('     DATABASE INITIALIZED')
                print('--------------------------------')
            else:
                print(f'||||| INITIALIZATION FAILED: {self.db_path} |||||')
                
            return initialized
        except Exception as e:
            print(e)
            return
    
    def read(self) -> list:
        """Fetches all the data from the file it reads.

        Returns:
            list: data from the files
        """        
        try:
            with open(self.db_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(e)
            return
        
    def __write(self, data: list) -> bool:
        """[PRIVATE METHOD]
        This overwrites all contents of the file. It should not be used
        on its own, but as a companion to the the other methods.

        Args:
            data (list): The data that replaces the file's contents.

        Returns:
            bool: If writing over the file was successful.
        """        
        try:
            with open(self.db_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
                
            raw_data: list = self.read()
            
            return data == raw_data
        except Exception as e:
            print(e)
            return
        
    def add(self, data: dict) -> bool:
        """Adds a dictionary to the list of contents in the given file.
        The dictionary does not write over the whole file. The file contents
        are fetched, appended to, and then the updated contents are written.

        Returns:
            bool: If adding data was successful
        """        
        try:
            # fetch file contents
            raw_data: list = self.read()
            
            # append data
            raw_data.append(data)
            
            # write the edited raw_data
            self.__write(raw_data)
            
            # clear and refresh file contents
            raw_data = None
            raw_data = self.read()
            
            # validate success
            return data in raw_data
        except Exception as e:
            print(e)
            return
        
    def update(self, key: str, value: str, data: dict) -> bool:
        """Locates the target dict from the file contents and
        replaces it with the updated information.

        Args:
            key (str): The field used to search for the data
            value (str): The value of the field
            data (dict): The updated data 

        Returns:
            bool: If the update was successful
        """
        try:
            # fetch file contents
            raw_data: list = self.read()
            
            # locate target item
            target: dict = None

            for item in raw_data:
                if item[key] == value:
                    target = item
                    break

            # remove and replace
            raw_data.remove(target)
            raw_data.append(data)
            
            # write data to file
            self.__write(raw_data)
            
            # clear and refresh file contents
            raw_data = None
            raw_data = self.read()
            
            # validate success
            return data in raw_data and target not in raw_data
        except Exception as e:
            print(e)
            return
        
    def delete(self, key: str, value: str) -> bool:
        """Removes an item from the file contents.

        Args:
            key (str): The field used to search for the data
            value (str): The value of the field

        Returns:
            bool: If the deletion was successful
        """
        try:
            # fetch file contents
            raw_data: list = self.read()
            
            # locate target item
            target: dict = None
            
            for item in raw_data:
                if item[key] == value:
                    target = item
                    break

            # remove
            raw_data.remove(target)
            
            # write data to the file
            self.__write(raw_data)
            
            # clear and refresh file contents
            raw_data = None
            raw_data = self.read()
            
            # validate success
            return target not in raw_data
        except Exception as e:
            print(e)
            return
    