from fastapi import APIRouter
from api.schemas.user import User, UserCreate, UserUpdate
from api.models.user import UserModel
from fastapi import HTTPException, status
from fastapi.responses import Response
from api.services.user import UserService
router = APIRouter(prefix='/usuario', tags=['usuarios'])

@router.get("/", response_model=list[User])
def list_users():
    return UserModel.get_all()

@router.get("/{user_id}", response_model=User)
def get_user(user_id: str):
    user = UserModel.get_by_id(user_id)
    if user == None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado!")
    return user

@router.post("/", response_model=User)
def create_user(user_data: UserCreate):
    return UserModel.create(user_data.model_dump())

@router.put("/{user_id}", response_model=User)
def update_user(user_id: str, user_data: UserUpdate):
    user = UserModel.update(user_id, user_data.model_dump(exclude_unset=True))
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    sucess = UserModel.delete(user_id)
    if not sucess:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{user_id}/passar", response_model=User)
def user_swipe_card(user_id: str):
    return UserService.user_swipe_card(user_id)

@router.post("/{user_id}/recarregar", response_model=User)
def user_recharge(user_id:str, recharge_info:dict):
    return UserService.user_recharge(user_id, recharge_info)

