from api.models.base import BaseModel
from typing import Dict

class RestaurantModel(BaseModel):

    @classmethod
    def get_all(cls) -> list[Dict[str, dict]]:
        db = cls._read_db()
        return [{"id":r_id, **r_data} for r_id, r_data in db.get("restaurants", {}).items()];

    @classmethod
    def get_by_id(cls, restaurant_id: int):
        restaurants = cls.get_all()
        return next((r for r in restaurants if r["id"] == restaurant_id), None)
    
    @classmethod
    def create(cls, restaurant_data: dict):
        db = cls._read_db()
        restaurants = db.get("restaurants",{})
        next_id = str(len(restaurants))
        restaurants[next_id] = restaurant_data
        db["restaurants"] = restaurants
        cls._write_db(db)
        return {"id":next_id, **restaurant_data}

    @classmethod
    def update(cls, restaurant_id: str, restaurant_data: dict):
        db = cls._read_db()
        restaurants = db.get("restaurants",{})

        if restaurant_id in restaurants:
            restaurants[restaurant_id].update(restaurant_data  )
            db["restaurants"] = restaurants
            cls._write_db(db)
            return cls.get_by_id(restaurant_id)
        else:
            return None
        
    @classmethod
    def delete(cls, restaurant_id):
        db = cls._read_db()
        restaurants = db.get("restaurants",{})

        if restaurant_id in restaurants:
            del restaurants[restaurant_id]
            db["restaurants"] = restaurants
            cls._write_db(db)
            return True
        else:
            return False
