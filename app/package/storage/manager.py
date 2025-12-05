import yaml
from .factory import StorageFactory

class StorageManager:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        
        self.relational_stores = {}
        self.nosql_stores = {}
        self._initialize_stores()
    
    def _initialize_stores(self):
        # Initialize relational stores
        if "relational" in self.config:
            for name, config in self.config["relational"].items():
                self.relational_stores[name] = StorageFactory.create_relational(
                    config["type"], config["config"]
                )
        
        # Initialize NoSQL stores
        if "nosql" in self.config:
            for name, config in self.config["nosql"].items():
                self.nosql_stores[name] = StorageFactory.create_nosql(
                    config["type"], config["config"]
                )
    
    def get_relational(self, name: str):
        return self.relational_stores[name]
    
    def get_nosql(self, name: str):
        return self.nosql_stores[name]