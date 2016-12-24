import sys, os

def load():
    dependencies_directory = os.path.join(os.path.dirname(__file__), "..", "dependencies")
    dependencies = os.listdir(dependencies_directory)
    for directory in dependencies:
        if not directory.startswith("."):
            sys.path.append(dependencies_directory + "/" + directory)

    sys.path.append((os.path.join(os.path.dirname(__file__), "..", "src")))
