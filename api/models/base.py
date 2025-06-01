import json
from api.core.config import DB_PATH
from typing import Dict

class BaseModel:
    @staticmethod
    def _read_db() -> Dict:
        with open(DB_PATH, 'r') as f:
            return json.load(f);

    @staticmethod
    def _write_db(data: Dict) -> None:
        with open(DB_PATH, 'w') as f:
            json.dump(data, f, indent=4)