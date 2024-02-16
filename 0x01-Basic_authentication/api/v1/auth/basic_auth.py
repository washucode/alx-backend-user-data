#!/usr/bin/env python3

"""
Basic authentication module
"""

from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User


class BasicAuth(Auth):
    """
    Basic authentication class
    """
    def __init__(self) -> None:
        super().__init__()

    def extract_base64_authorization_header(self,
                                            authorization_header:
                                            str) -> str:
        """
        Public method to extract base64 authorization header
        """
        if authorization_header is\
                None or type(authorization_header) is not str:
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        Public method to decode base64 authorization header
        """
        if base64_authorization_header is None\
                or type(base64_authorization_header) is not str:
            return None
        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Public method to extract user credentials
        """
        if decoded_base64_authorization_header\
                is None or\
                type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1)
                     )

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Public method to create user object from credentials
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            user_exists = List[TypeVar('User')]
            user_exists = User.search({'email': user_email})
        except Exception:
            return None

        for user in user_exists:
            if user.is_valid_password(user_pwd):
                return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Public method to require current user
        """
        auth_header: str = self.authorization_header(request)

        if auth_header is None:
            return None
        
        base64_auth_header: str = self.extract_base64_authorization_header(
            auth_header)
        
        if base64_auth_header is None:
            return None
        
        decoded_auth_header: str = self.decode_base64_authorization_header(
            base64_auth_header)
        
        if decoded_auth_header is None:
            return decoded_auth_header
        
        email: str
        pwd: str
        email, pwd = self.extract_user_credentials(
            decoded_auth_header)
        
        if email is None or pwd is None:
            return None
        
        curr_user = self.user_object_from_credentials(email, pwd)

        return curr_user
