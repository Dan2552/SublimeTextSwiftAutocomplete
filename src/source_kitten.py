import subprocess
from subprocess import Popen, PIPE, STDOUT
import ijson
import shlex
import swift_project
import cached_invoke

def complete(offset, file, project_directory, text):
    source_files = swift_project.source_files(project_directory)
    source_files = _filter_file_from_list(file, source_files)
    source_files = map(_escape_spaces, source_files)

    calculated_offset = _calculate_source_kitten_compatible_offset(offset, text)
    text = _cut_calculated_offset_difference(offset, calculated_offset, text)

    cached_invoke_cmd = _escape_spaces(cached_invoke.executable_path()) + " 5 "
    navigate_to_project = "cd " + project_directory
    command = " sourcekitten complete"
    arg_file = " --text " + shlex.quote(text)
    arg_offset = " --offset " + str(calculated_offset)
    arg_sdk = " -sdk /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator10.2.sdk"
    arg_target = " -target x86_64-apple-ios9.0"
    arg_files = " " + " ".join(source_files)

    cmd = cached_invoke_cmd + \
          navigate_to_project + \
          " &&" + \
          command + \
          arg_file + \
          arg_offset + \
          " --" + \
          arg_sdk + \
          arg_target + \
          arg_files

    with Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT) as p:
      try:
          results = list(ijson.items(p.stdout,''))[0]
          return results
      except ijson.backends.python.UnexpectedSymbol:
          return []

# When a file is unsaved, you don't want the persisted file passed into
# SourceKitten
def _filter_file_from_list(file, source_files):
    return filter(lambda x: x != file, source_files)

def _escape_spaces(str):
    return str.replace(" ", "\ ")

# If you try to autocomplete midword, SourceKitten returns no results, so this
# function will calculate an offset that will potentially return results
def _calculate_source_kitten_compatible_offset(offset, text):
    trimmed_off_left = 0

    # Trim the text down
    text = text[0:offset]

    # Trim off the left, from the last newline
    newline_index = text.rfind("\n", 0, len(text))
    text = text[(newline_index + 1):len(text)]
    trimmed_off_left = trimmed_off_left + newline_index + 1

    # Trim off the left, if there is a ; on this line
    if ";" in text:
      semicolon_index = text.rfind(";", 0, len(text))
      text = text[(semicolon_index + 1):len(text)]
      trimmed_off_left = trimmed_off_left + semicolon_index + 1

    last_dot_location = text.rfind(".", 0, len(text))
    last_space_location = text.rfind(" ", 0, len(text))


    if last_dot_location > last_space_location:
        offset = trimmed_off_left + last_dot_location + 1
    elif last_space_location > -1:
        offset = trimmed_off_left + last_space_location + 1

    # # Uncomment for some really useful debug printing:
    # print("\n" + text)
    # print(((offset - trimmed_off_left - 1) * " ") + "^")

    return offset

# By cutting the offset difference, the same command will be triggered to
# SourceKitten which will then take advantage of cached_invoke
def _cut_calculated_offset_difference(offset, calculated_offset, text):
    left = text[0:calculated_offset]
    right = text[offset:len(text)]
    return left + right
