import subprocess
from subprocess import Popen, PIPE, STDOUT
import ijson
import shlex
import swift_project

def complete(offset, file, project_directory, text):
  print("complete is run")

  source_files = swift_project.source_files(project_directory)
  print(type(source_files))
  source_files = _filter_file_from_list(file, source_files)

  navigate_to_project = "cd " + project_directory
  command = " sourcekitten complete"
  arg_file = " --text " + shlex.quote(text)
  arg_offset = " --offset " + str(offset)
  arg_sdk = " -sdk /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator10.2.sdk"
  arg_target = " -target x86_64-apple-ios9.0"
  arg_files = " " + " ".join(source_files).replace("\n", "")

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

def _filter_file_from_list(file, source_files):
  return filter(lambda x: x != file, source_files)
