#!/usr/bin/env python3
"""Module for session expiration
"""


import os
from datetime import datetime as dt, timedelta

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth is a class that
    adds session expiration to the authentication mechanism
    """

    def __init__(self):
        """
        Constructor for the SessionExpAuth class
        """
        super().__init__()

        self.session_duration = int(os.environ.get("SESSION_DURATION", 0))

    def create_session(self, user_id: int) -> str:
        """Creates a new session for a user and assigns a session ID

        Args:
            user_id (int): The id of the user to create a session for

        Returns:
            str: The session ID if the session was successfully creayed
        """
        sessn_id = super().create_session(user_id)
        if sessn_id is None:
            return None
        self.user_id_by_session_id[sessn_id] = {
            'user_id': user_id,
            'created_at': dt.now()
        }
        return sessn_id

    def user_id_for_session_id(self, session_id: str) -> int:
        """Gets the user_id associated with a session ID

        Args:
            session_id (str): The session ID to get the user_id for

        Returns:
            int: The user_id associated with the session ID if the session is
        valid..
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict.get("user_id")
        created_at = session_dict.get('created_at')
        if created_at is None:
            return None
        now = dt.now()
        if created_at + timedelta(seconds=self.session_duration) < now:
            return None
        expires_at = session_dict["created_at"] + \
            timedelta(seconds=self.session_duration)
        if expires_at < dt.now():
            return None
        return session_dict.get("user_id", None)
