import sqlite3
from sqlite3 import Error

class Database:
  _instance = None

  def __new__(cls, db_file):
    if cls._instance is None:
      cls._instance = super(Database, cls).__new__(cls)

  cls._instance._initialize(self, db_file)
    return cls._instance
return cls._instance
