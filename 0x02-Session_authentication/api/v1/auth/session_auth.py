#!/usr/bin/env python3
"""
Session Authentication
"""

from api.v1.auth.auth import Auth
from models.user import User
import uuid
from typing import TypeVar
import base64


class SessionAuth(Auth):
    """session authentication
    """
    def __init__(self) -> None:
        """constructor
        """
        super().__init__()

    user_id_by_session_id = {}

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def create_session(self, user_id: str = None) -> str:
        """creates a session
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def destroy_session(self, request=None) -> bool:
        """destroys a session
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
