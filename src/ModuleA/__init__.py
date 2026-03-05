"""
Module A
-------------------------
This is a sample module which has class for Sample things

"""

class DatabaseA(object):
    """
    Sample class which is something
    """
    def __init__(self, connection_string):
        """_summary_
        This is connection string to something
        Args:
            connection_string (_type_): str
        """
        self.connection_string = connection_string
    
    def connectA(self) -> True:
        """_summary_
        This some connection method
        Returns:
            True: _description_
        """
        print("connected to database")
        return True