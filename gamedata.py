###############
# DO NOT EDIT #
###############

class GameData:
    '''
    A class that is used as a "data base" for the game. It allows the game
    to store and retreive any data that is needed for the game to run. It is useful
    to hold information about the game state, such as settings, player data, etc.
    '''

    def __init__(self):
        self.dbase = {}

    def setData(self, name: str, value: any):
        '''
        Set the data with the name `name` to the value `value`. If the data
        already exists, it will be overwritten with the new value.
        
        Args:
            name (str): The name of the data to be stored
            value (any): The value of the data to be stored
        '''
        self.dbase[name] = value

    def getData(self, name: str):
        '''
        Get the data with the name `name`. If the data does not exist, it will
        return ``None``.

        Args:
            name (str): The name of the data to be retrieved
        
        Returns:
            any: The value of the data with the name `name`.
        '''
        if name in self.dbase: 
            return self.dbase[name]
        else:
            return None

    def isData(self, name: str, value: any):
        '''
        Check if the data with the name `name` is equal to the value `value`.
        If the data does not exist, it will return ``False``.
        
        Args:
            name (str): The name of the data to be checked
            value (any): The value to be checked against
            
        Returns:
            bool: True if the data with the name `name` is equal to the value `value`
        '''
        if name in self.dbase:
            return self.dbase[name] == value
        else:
            return False

###############
# DO NOT EDIT #
###############