class DataDimensionException(Exception):
    def __init__(self):
        Exception.__init__(self, "Data must be either a 1-dimensional list or 2 1-dimensional lists in a 2-dimensional list")

##class DataLengthException(Exception):
##    def __init__(self):
##        Exception.__init__(self, "Data must consist of 1 or 2 1-dimensional lists")

class DataDifferentLengthException(Exception):
    def __init__(self):
        Exception.__init__(self, "Data sets must be same length")

class DataTypeException(Exception):
    def __init__(self):
        Exception.__init__(self, "Data in lists must be ints or floats")

class BadPowerException(Exception):
    def __init__(self):
        Exception.__init__(self, "Power must be less that max data points+1")
