import os

def data_directory():
    return os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', "data"))
