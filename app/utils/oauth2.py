from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.token import verify_token


ouath2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def get_current_user(token: Annotated[str, Depends(ouath2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(token, credentials_exception)


# async def get_current_active_user(
#     current_user: Annotated[AuthOutOut, Depends(get_current_user)]
# ):
# if current_user.disabled:
#     raise HTTPException(status_code=400, detail="Inactive user")
# return current_user
