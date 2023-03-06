from fastapi import HTTPException, Depends
from fastapi import APIRouter
from fastapi_jwt_auth import AuthJWT
from .models import User
from .config import settings

router = APIRouter(prefix="/auth",
                   tags=["auth"],
                   responses={404: {"description": "Not found"}},)


@AuthJWT.load_config
def get_config():
    return settings


@router.post('/login')
def login(user: User, Authorize: AuthJWT = Depends()):
    # Test with user with username is test and password is test
    if user.username == "test" and user.password == "test":
        # Render access token and refresh token
        access_token = Authorize.create_access_token(subject=user.username)
        refresh_token = Authorize.create_refresh_token(subject=user.username)
        return {"access_token": access_token, "refresh_token": refresh_token}

    raise HTTPException(status_code=401, detail="Bad username or password")


@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)

    return {"access_token": new_access_token}


@router.get('/protected')
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}
