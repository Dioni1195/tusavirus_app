#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.base_model import BaseModel, Base
from models.state import State
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        database = getenv('DATABASE_URL')
        self.__engine = create_engine('{}'.format(database))

    def all(self):
        """query on the current database session"""
        new_dict = {}
        objs = self.__session.query(State).all()
        for obj in objs:
            key = obj.name
            new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, id):
        """ Returns the object based on the class name and its ID,
        or None if not found """
        name = "{}".format(id)
        if name in self.all():
            return self.all()[name]

    def count(self):
        """ Returns the number of objects. """
        count = 0
        for state in self.all().values():
            count += state.victims
        return(count)
