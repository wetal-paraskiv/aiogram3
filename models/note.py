""" Module for creating postgres tables """

from sqlalchemy import Column, Integer, String
from db.engine import Base


class Note(Base):
    """ Note class for notes table """
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, nullable=False)
    note = Column(String)
    user_id = Column(String)

    def __init__(self, note, user_id):
        """"""
        self.note = note
        self.user_id = user_id
