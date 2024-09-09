#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar, Dict
from sqlalchemy.exc import NoResultFound, InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session
    
    def add_user(self, email: str, hashed_password: str) -> TypeVar[User]:
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        return user
    
    def find_user_by(self, **kwargs: Dict[str, str]) -> TypeVar[User]:
        """Finds a user based on arbitrary keyword arguments
        
        Raises:
            NoResultFound: If no user matches the criteria
            InvalidRequestError: If invalid query arguments are passed
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            
            if user is None:
                raise NoResultFound
            
            return user
        
        except InvalidRequestError as e:
            raise InvalidRequestError from e
        
    def update_user(self, user_id: int, **kwargs: Dict[str, str]) -> None:
        """Finds user with some specified id and updates
        the user with passed in keyword arguments"""
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if not hasattr(user, key):
                    raise ValueError(f"User has no attribute '{key}'")
                
                setattr(user, key, value)
            self._session.commit()
        
        except NoResultFound:
            raise ValueError("User not found")
        