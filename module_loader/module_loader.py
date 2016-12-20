moduleDirectories = [
  "lib"
]

# Special thanks to https://github.com/Enteleform
# from https://github.com/Enteleform/-SCRIPTS-/tree/master/SublimeText/Module_Loader

import imp, os, sys
parentDirectory = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

def load(pluginGlobals):
  moduleExtensions  = [ "py" ] # add extensions here to extend module support
  moduleLoader_Name = "module_loader"
  modulePaths       = []

  for directory in moduleDirectories:
    modulePaths.append(parentDirectory + os.sep + directory)

  for index in range(0, 2): # loads modules twice to ensure dependencies are updated
    for path in modulePaths:
      for file in os.listdir(path):
        for extension in moduleExtensions:

          if file.endswith(os.extsep + extension):
            moduleName = os.path.basename(file)[: - len(os.extsep + extension)]

            if moduleName != moduleLoader_Name:
              fileObject, file, description = imp.find_module(moduleName, [path])
              pluginGlobals[moduleName] = imp.load_module(moduleName, fileObject, file, description)


