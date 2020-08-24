from typing import Union
from pymongo.results import UpdateResult, InsertOneResult 
from umongo import Document, fields, validate
from marshmallow.exceptions import ValidationError

from modules.common.utils import get_now
from modules.database import mongo_instance
from modules.common.constants import ON_CLEANING, BEFORE_CLEANING
from modules.database.models import ListModel, create_list

@mongo_instance.register
class UserModel(Document):
    buylist = fields.ReferenceField(ListModel, default=None)
    chat_id = fields.IntField(required=True, unique=True)
    username = fields.StrField()
    #lastnotice = fields.DateTimeField(default=get_now())
    checknotice = fields.BoolField(default=True)
    chosenbuilding = fields.IntField(default=0)
    noticehour = fields.IntField(default=8)
    notification = fields.DictField(
        default={
            BEFORE_CLEANING: None,
            ON_CLEANING: 8
            }
        )
    lastnotice = fields.DictField(
        default={
            BEFORE_CLEANING: get_now(),
            ON_CLEANING: get_now()
            }
        )

    class Meta:
        collection_name = 'user'


    def update(self, **attrs) -> Union[UpdateResult, InsertOneResult]:
        for attr in attrs:
            self[attr] = attrs[attr]
        return self.commit()

    def get_buy_list(self) -> ListModel:
        try:
            return self.buylist.fetch()
        except ValidationError:
            _list = create_list(self.chat_id)
            self.update(buylist=_list)
            return _list


def __create_user(chat_id) -> UserModel:
    '''
    Create User with default parameters
    '''
    user = UserModel(chat_id=chat_id)
    _list = create_list(chat_id)
    user.update(buylist=_list)

    user.required_validate()
    return user

def create_user_if_not_exists(chat_id) -> UserModel:
    '''
    Return User with chat_id, if not found, create one
    '''
    user = find_user({'chat_id': chat_id})
    if not user:
        user = __create_user(chat_id)
    return user

def find_user(dct: dict) -> UserModel:
    '''
    Find user
    '''
    return UserModel.find_one(dct)