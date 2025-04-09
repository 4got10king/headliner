from abc import abstractmethod

from pydantic import BaseModel
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    @abstractmethod
    def get_schema(self) -> BaseModel:
        raise NotImplementedError

    @classmethod
    def get_related(self):
        return inspect(self).relationships.items()
