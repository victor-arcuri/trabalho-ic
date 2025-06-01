from api.models.restaurant import RestaurantModel
from fastapi import HTTPException
class RestaurantService:

    @staticmethod
    def enter_restaurant(restaurant_id: str):
        restaurant = RestaurantModel.get_by_id(restaurant_id)
        if restaurant == None:
            return None
        restaurant["occupancy"] += 1
        db = RestaurantModel._read_db()
        restaurants = db.get("restaurants", {})
        restaurants[restaurant_id] = restaurant
        db["restaurants"] = restaurants
        RestaurantModel._write_db(db)
        return restaurant
    
    @staticmethod
    def exit_restaurant(restaurant_id: str):
        restaurant = RestaurantModel.get_by_id(restaurant_id)
        if restaurant == None:
            return None
        if restaurant["occupancy"] > 0:
            restaurant["occupancy"] -= 1
        else:
            raise HTTPException(status_code=400, detail="Restaurante não pode ter lotação negativa!")
        db = RestaurantModel._read_db()
        restaurants = db.get("restaurants", {})
        restaurants[restaurant_id] = restaurant
        db["restaurants"] = restaurants
        RestaurantModel._write_db(db)
        return restaurant
        
        