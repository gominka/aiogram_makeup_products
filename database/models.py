import datetime

from peewee import (
    AutoField,
    CharField,
    DateTimeField,
    IntegerField,
    Model,
    SqliteDatabase,
)

from config_data.config import DB_NAME

db = SqliteDatabase(DB_NAME)


class BaseModel(Model):
    """Base Model"""

    class Meta:
        database = db


class User(BaseModel):
    """Model of users"""

    user_id = IntegerField(unique=True)
    username = CharField()
    first_name = CharField()

    def __str__(self):
        return f"{self.user_id} - {self.username}"


class History(BaseModel):
    """Model of users selections"""

    select_id = AutoField()
    user_id = IntegerField()
    product_name = CharField()
    selection_date = DateTimeField(default=datetime.datetime.now)


def create_models():
    db.create_tables(BaseModel.__subclasses__(), safe=True)
