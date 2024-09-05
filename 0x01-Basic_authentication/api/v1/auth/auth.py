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
        if path is None or not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
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
