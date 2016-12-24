import sys, os
sys.path.append("../..")

from SourceKittenSubl.dependencies import dependencies
dependencies.load()

# allows import of helpers
sys.path.append(os.path.dirname(__file__))
