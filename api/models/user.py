from base import BaseModel
from typing import Dict

class UserModel(BaseModel):

    @classmethod
    def get_all(cls) -> Dict[str, dict]:
        db = cls._read_db()
        return db.get("users", {});

    @classmethod
    def get_by_id(cls, user_id: int):
        users = cls.get_all()
        return next((u for u in users if u["id"] == user_id), None)
    
    @classmethod
    def create(cls, user_data: dict):
        db = cls._read_db()
        users = cls.get_all()
        
        next_id = str(len(users))

        users[next_id] = user_data
        db["users"] = users

        cls._write_db(db)
        return {next_id: user_data}

    @classmethod
    def update(cls, user_id: str, user_data: dict):
        db = cls._read_db()
        users = cls.get_all()

        if user_id in users:
            users[user_id].update(user_data)
            db["users"] = users
            cls._write_db(db)
            return users[user_id]
        else:
            return None
        
    @classmethod
    def delete(cls, user_id):
        db = cls._read_db()
        users = cls.get_all()

        if user_id in users:
            del users[user_id]
            db["users"] = users
            cls._write_db(db)
            return True
        else:
            return False
