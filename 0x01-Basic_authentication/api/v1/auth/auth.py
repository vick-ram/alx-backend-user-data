#!/usr/bin/env python3
"""auth module"""
from flask import request
from typing import List, TypeVar


class Auth:
    """auth class"""

    def require_auth(
        self,
        path: str,
        excluded_paths: List[str]
    ) -> bool:
        """returns False - path"""
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        if not path.endswith('/'):
            path += '/'

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """Returns the authorization header from the request."""
        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """returns nothing"""
        return None
