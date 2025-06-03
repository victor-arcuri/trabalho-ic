from api.models.user import UserModel
from fastapi import HTTPException

class UserService:
    @staticmethod
    def user_swipe_card(user_id: str):
        user =  UserModel.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado!")
        fumpLevel = user["fump"]
        balance = user["balance"]

        if fumpLevel == 5:
            price = 290
        elif fumpLevel == 4:
            price = 200
        elif fumpLevel == 2 or fumpLevel == 3:
            price = 100
        elif fumpLevel == 1:
            price = 0
        elif fumpLevel == 0:
            price = 560
        if (balance - price < 0):
            raise HTTPException(status_code=400, detail="Dinheiro insuficiente")
        balance -= price
        return UserModel.update(user_id,{"balance":balance}) 
    
    @staticmethod
    def user_recharge(user_id: str, recharge_info:dict):
        amount = recharge_info.get("amount", None)
        if amount is None:
            raise HTTPException(status_code=400, detail="Montante não especificado!")
        user =  UserModel.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado!")
        balance = user["balance"]
        return UserModel.update(user_id,{"balance":balance+amount}) 
    
    def fump_info(user_id: str):
        user =  UserModel.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado!")
        
        fumpLevel = user["fump"]
        if fumpLevel == 5:
            price = 290
            level = "IV-B"
        elif fumpLevel == 4:
            price = 200
            level = "IV-A"
        elif fumpLevel == 3:
            price = 100
            level = "III"
        elif fumpLevel == 2:
            price = 100
            level = "II"
        elif fumpLevel == 1:
            price = 0
            level = "I"
        elif fumpLevel == 0:
            level = "Sem posicionamento pela FUMP"
            price = 560
        
        return {"price":price, "level":level}
        

        
        
        
