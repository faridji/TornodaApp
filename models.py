# this is not the complete models.py, but enough to see the differences
from tornado_sqlalchemy import declarative_base

Base = declarative_base


class Task(Base):
    def test(self):
        print("test")
