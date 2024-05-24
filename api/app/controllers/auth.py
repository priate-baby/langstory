from typing import Optional
from uuid import UUID
from datetime import datetime, timezone, timedelta
import jwt
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from app.logger import get_logger
from app.settings import settings
from app.models.user import User
from app.models.organization import Organization
from app.schemas.user_schemas import ScopedUser
from app.schemas.jtw_schema import JWTBase, JWTResponse
from app.http_errors import forbidden, unauthorized

from app.controllers.mixins.password_mixin import PasswordMixin
from app.controllers.mixins.auth_mixin import AuthMixin

logger = get_logger(__name__)


class AuthenticateUsernamePasswordFlow(AuthMixin, PasswordMixin):
    """authenticate the user with username and password"""

    def authenticate(self, email_address: str, password: str) -> User:
        """authenticate the user or raise an exception"""
        try:
            user = User.read(self.db_session, email_address=email_address)
            if self.password_context.verify(password, user.password):
                return user
            raise ValueError("password is incorrect")
        except (MultipleResultsFound, NoResultFound, ValueError) as e:
            unauthorized(e=e, message="User not found or password is incorrect")

class JWTTokenFlow(AuthMixin):
    algorithm: str = "HS256"

    def get_refresh_token(self, user: User) -> "JWTResponse":
        """generates a bare refresh token for a given user"""
        logger.debug("generating refresh token for %s", user.email_address)
        expire = datetime.now(timezone.utc) + timedelta(days=365)
        data = {"sub": user.id, "exp": expire}
        token = jwt.encode(
            data.copy(), settings.jwt_secret_key, algorithm=self.algorithm
        )
        logger.debug(
            "refresh token for %s created, expires %s", user.email_address, expire
        )
        return JWTResponse(token=token, data=data)

    def get_auth_token(
            self, refresh_token: "JWTBase", org: Optional["str"] = None
    ) -> "JWTResponse":
        """generate a detailed token and readable data for a given user and org"""
        decoded = jwt.decode(
            refresh_token.token, settings.jwt_secret_key, algorithms=[self.algorithm]
        )
        assert decoded["exp"] > datetime.now(timezone.utc).timestamp(), "token is expired"
        try:
            user = User.read(self.db_session, id_=decoded["sub"])
        except (MultipleResultsFound, NoResultFound, ValueError) as e:
            unauthorized(e=e, message="User not found")
        org_data = {}
        if org:
            org_uid = self.get_org_uid(org)
            sql_org = Organization.read(self.db_session, uid=org_uid)
            try:
                assert (
                        sql_org in user.organizations
                ), f"User {user.uid} is not a member of org {org}"
            except AssertionError as e:
                forbidden(
                    e=e,
                    message="User does not belong to this organization or it does not exist",
                )
            org_data = {
                "id": sql_org.id,
                "name": sql_org.name,
            }
        expire = datetime.now(timezone.utc) + timedelta(minutes=5)
        user_data = {
            "id": user.id,
            "email_address": user.email_address,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "avatar_url": user.avatar_url,
            "organizations": [o.id for o in user.organizations],
        }
        data = {
            "sub": user.id,
            "org": org_data,
            "exp": expire,
            "user": user_data,
        }
        token = jwt.encode(data.copy(), settings.jwt_secret_key, algorithm=self.algorithm)
        return JWTResponse(token=token, data=data)

    def get_scoped_user(cls, token: str) -> ScopedUser:
        """get a user object from a token"""
        decoded = jwt.decode(token, settings.jwt_secret_key, algorithms=[cls.algorithm])
        user_uid = UUID(decoded["sub"].split("user-")[1])
        org = None
        if decoded["org"]:
            org_uid = cls.get_org_uid(decoded["org"]["id"])
            org = Organization(uid=org_uid, name=decoded["org"]["name"])
        return ScopedUser(
            user=User(uid=user_uid, email_address=decoded["user"]["email_address"]),
            organization=org,
        )