from typing import Annotated, Generator, Optional
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.settings import settings
from app.schemas.jtw_schema import JWTResponse
from app.routers.utilities import get_db_session
from app.schemas.user_schemas import NewUser
from app.models.all import Organization
from app.controllers.auth import JWTTokenFlow, AuthenticateUsernamePasswordFlow
from app.controllers.user import CreateNewUserFlow


router = APIRouter(prefix="/auth/username-password", tags=["auth"])


@router.post("/sign-up")
async def sign_up(
    new_user: NewUser,
    db_session: Annotated["Generator", Depends(get_db_session)],
) -> Optional[JWTResponse]:
    """register a new user"""
    user = CreateNewUserFlow(db_session).create_user_with_username_password(new_user)
    return JWTTokenFlow(db_session).get_refresh_token(user)


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: Annotated["Generator", Depends(get_db_session)],
) -> Optional[JWTResponse]:
    """use standard U/P to exchange for a refresh JWT"""
    user = AuthenticateUsernamePasswordFlow(db_session).authenticate(
        email_address=form_data.username, password=form_data.password
    )
    return JWTTokenFlow(db_session).get_refresh_token(user)


@router.post("/dev-login")
async def development_only_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: Annotated["Generator", Depends(get_db_session)],
):
    """for local development only! get a long-running primary auth token"""
    if not settings.environment == "dev":
        raise ValueError("this endpoint is only available in local development")
    user = AuthenticateUsernamePasswordFlow(db_session).authenticate(
        email_address=form_data.username, password=form_data.password
    )
    flow = JWTTokenFlow(db_session)
    refresh = flow.get_refresh_token(user)
    org = Organization.default(db_session)
    auth_token = flow.get_auth_token(
        refresh, org=org.id, expire_min=(60 * 24 * 365)
    ).token
    return {"access_token": auth_token, "token_type": "bearer"}
