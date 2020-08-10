from datetime import datetime
from misc import logger
from modules.common.constants import MAX_ITEM_LENGTH

class List:
    '''
    list structure: {
        '<<item name>>': {
            'amount': 1,
            'date': datetime.datetime()
        }
    }
    '''

    @staticmethod
    def default():
        return {'Sample': {
            'amount': 0,
            'date': str(datetime.now())
        }}

    def __init__(self, user, **kwargs):
        self.user = user
        self.current_list = self.__get_list()

    def __get_list(self) -> dict:
        '''
        Returns current list from database
        '''
        return self.user.get('list')

    def __update(self) -> bool:
        '''
        Update value in database

        Returns bool as result of work
        '''
        return self.user.update(list=self.current_list)

    def add(self, items: list) -> bool:
        '''
        Add all items to list. 
        If it already exists, increment amount
        '''
        for item in items:

            if len(item) > MAX_ITEM_LENGTH:
                return False

            self.current_list.setdefault(item, 
                List.default()['Sample']
                )

        for item in items:
            self.current_list[item]['amount'] += 1

        return self.__update()

    def clear(self) -> bool:
        '''
        Completely clear the list
        '''
        self.current_list = {}
        return self.__update()

    def content(self) -> list:
        '''
        Returns list in such way sorted by date:
        [ ('<<item name>>', 1), ( ... ) ]
        '''

        # item names, sorted by date
        sorted_names = sorted(
            self.current_list, 
            key=lambda name: self.current_list[name]['date'])
        
        result_list = [
            (name, self.current_list[name]['amount']) 
                for name in sorted_names
                ]

        return result_list

    def change_amount(self, item_name: str, number: int) -> bool:
        '''
        Set `amount` = `amount` + `number`
        If new amount less than one, then delete it
        
        Returns bool as result of work
        '''
        if item_name in self.current_list:
            self.current_list[item_name]['amount'] += number

            if self.current_list[item_name]['amount'] <= 0:
                self.current_list.pop(item_name)
        
            return self.__update()
        
        else:
            return False