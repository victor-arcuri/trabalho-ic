from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
from api.schemas.restaurant import Restaurant, RestaurantUpdate, RestaurantCreate
from api.models.restaurant import RestaurantModel
from api.services.restaurant import RestaurantService
router = APIRouter(prefix="/restaurante", tags=["restaurants"])

# Pega todos os restaurantes 
@router.get("/", response_model=list[Restaurant])
def list_restaurants():
    return RestaurantModel.get_all()

# Mostra o restaurante do id especificado
@router.get("/{restaurant_id}",response_model=Restaurant)
def get_restaurant(restaurant_id: str):
    restaurante = RestaurantModel.get_by_id(restaurant_id)
    if restaurante is None:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    return restaurante
# Atualiza o restaurante do id especificado
@router.put("/{restaurant_id}",response_model=Restaurant)
def update_restaurant(restaurant_id: str, restaurant_data: RestaurantUpdate):
    restaurant = RestaurantModel.update(restaurant_id, restaurant_data.model_dump(exclude_unset=True))
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    return restaurant

# Cria um novo restaurante com as informações passadas
@router.post("/", response_model=Restaurant)
def create_restaurant(restaurant: RestaurantCreate):
    return RestaurantModel.create(restaurant.model_dump())

# Deleta um restaurante com as informações passadas
@router.delete("/{restaurant_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(restaurant_id: str):
    sucess = RestaurantModel.delete(restaurant_id)
    if not sucess:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Aumenta a lotação de um restaurante em uma pessoa
@router.post("/{restaurant_id}/entrar",response_model=Restaurant)
def enter_restaurant(restaurant_id: str):
    restaurant = RestaurantService.enter_restaurant(restaurant_id)
    if restaurant == None:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    return restaurant;
    

# Reduz a lotação de um restaurante em uma pessoa
@router.post("/{restaurant_id}/sair",response_model=Restaurant)
def exit_restaurant(restaurant_id: str):
    restaurant = RestaurantService.exit_restaurant(restaurant_id)
    if restaurant == None:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    return restaurant;