dependencies = [
  "requests-2.12.4",
  "ijson-2.3"
]

import sys, os
for package in dependencies:
    path = os.path.join(os.path.dirname(__file__), "dependencies", package)
    sys.path.append(path)
