
class InvalidDetectionSubject(Exception):
    
    def __init__(self, expected, actual):
        super().__init__("Expected detection subject of type {}, Got {}".format(expected,actual))