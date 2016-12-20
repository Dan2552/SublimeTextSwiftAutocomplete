import subprocess
from subprocess import Popen, PIPE, STDOUT
import ijson

def complete(offset, file, project_directory):
  print("complete is run")

  navigate_to_project = "cd " + project_directory
  command = " sourcekitten complete"
  arg_file = " --file " + file
  arg_offset = " --offset " + str(offset)
  arg_sdk = " -sdk /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator10.2.sdk"
  arg_target = " -target x86_64-apple-ios9.0"
  arg_files = " $(find $(pwd) -name '*.swift')"

  cmd = navigate_to_project + \
        " &&" + \
        command + \
        arg_file + \
        arg_offset + \
        " --" + \
        arg_sdk + \
        arg_target + \
        arg_files

  p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
  print("running command: ")
  print(cmd)
  print("STDOUT:")
  print(p.stdout.peek())

  try:
    results = list(ijson.items(p.stdout,''))[0]
    return results
  except ijson.backends.python.UnexpectedSymbol:
    return []
