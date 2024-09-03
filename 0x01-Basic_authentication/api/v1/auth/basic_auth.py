#!/usr/bin/env python3
"""basic_auth module"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ Basic Authentication class that inherits from Auth """

    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """returns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """
        Decodes the Base64 part of the Authorization header.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        Extracts the user email and password from the Base64 decoded value.
        """
        if (decoded_base64_authorization_header is None or
            not isinstance(decoded_base64_authorization_header, str)):
    return None, None
       if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> TypeVar('User'):
        """
        Returns the User instance based on email and password.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        user_list = User.search({'email': user_email})
        if not user_list:
            return None

        user = user_list[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request.
        """
        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None

        base64_auth_header = self.extract_base64_authorization_header(
            authorization_header
        )
        if base64_auth_header is None:
            return None

        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header
        )
        if decoded_auth_header is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(
            decoded_auth_header
        )
        if user_email is None or user_pwd is None:
            return None

        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
