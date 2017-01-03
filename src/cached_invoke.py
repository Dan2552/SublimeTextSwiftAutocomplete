import os

def executable_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dependencies") + "/cached-invoke")
