from umongo import Document, fields, validate

from modules.common.utils import get_now
from modules.database import mongo_instance
from marshmallow.exceptions import ValidationError
    
from modules.database.models.List import create_list, List

@mongo_instance.register
class User(Document):
    buylist = fields.ReferenceField(List, default=None)
    chat_id = fields.IntField(required=True, unique=True)
    username = fields.StrField()
    lastnotice = fields.DateTimeField(default=get_now())
    checknotice = fields.BoolField(default=True)
    chosenbuilding = fields.IntField(default=0)
    noticehour = fields.IntField(default=8)

    class Meta:
        collection_name = 'user'


    def update(self, **attrs) -> None:
        for attr in attrs:
            self[attr] = attrs[attr]
        self.commit()

    def get_buy_list(self) -> List:
        try:
            return self.buylist.fetch()
        except ValidationError:
            _list = create_list(self.chat_id)
            self.update(buylist=_list)
            return _list

def get_user(chat_id, **kwargs) -> User:
    '''
    Return User with the following chat_id
    '''
    user = create_if_not_exists(chat_id=chat_id)
    user.update(**kwargs)
    return user




def __create_user(chat_id) -> User:
    '''
    Create User with default parameters
    '''
    user = User(chat_id=chat_id)
    _list = create_list(chat_id)
    user.update(buylist=_list)

    user.required_validate()
    return user

def create_if_not_exists(chat_id) -> User:
    '''
    Return User with chat_id, if not found, create one
    '''
    user = find_user({'chat_id': chat_id})
    if not user:
        user = __create_user(chat_id)
    return user

def find_user(dct: dict) -> User:
    '''
    Find user
    '''
    return User.find_one(dct)