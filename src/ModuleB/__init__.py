"""
Module B
-------------------------
This is a New module which has class for Sample things

"""

class DatabaseB(object):
    """
    Sample class which is something
    """
    def __init__(self, connect_string):
        """_summary_
        This is connection string to something
        Args:
            connection_string (_type_): str
        """
        self.connect_string = connect_string
    
    def connectB(self) -> True:
        """_summary_
        This some connection method
        Returns:
            True: _description_
        """
        print("connected to database")
        return True