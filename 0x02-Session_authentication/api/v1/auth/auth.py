#!/usr/bin/env python3
"""
Module for authentication
"""
from typing import List, TypeVar
import os
from flask import request


class Auth():
    """Template for all authentication system implemented in this app.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """This function takes a path and a list of excluded paths as arguments
        and returns a boolean value.

        Args:
            path (str): The path to check against the list of excluded paths
            excluded_paths (List[str]): The list of excluded paths

        Returns:
            bool: True if the path is not in the excluded paths list
            False otherwise
        """
        if not path:
            return True

        if not excluded_paths:
            return True

        path = path.rstrip("/")

        for excluded_path in excluded_paths:
            if excluded_path.endswith("*") and \
                    path.startswith(excluded_path[:-1]):
                return False
            elif path == excluded_path.rstrip("/"):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Gets the value of the Authorization header from the request

        Args:
            request (request, optional): Flask request obj

        Returns:
            str: The value of the Authorization header
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Mehtod that takes a request object as an optional argument
        and returns a value of type 'User'
        """
        return None

    def session_cookie(self, request=None) -> str:
        """Method to retrieve the session cookie from a request

        Args:
            request (flask.request, optional): Request to retrieve the session
            cookie

        Returns:
            str: The value of the session cookie
        """
        if request is not None:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
