import subprocess
from subprocess import Popen, PIPE, STDOUT
import ijson
import swift_project
import functools
import really_simple_yaml as yaml
import os

# Swift autocomplete. Calls `sourcekitten complete` with compiler argument
#
# - returns: A collection of suggestions
def complete(offset, file, project_directory, text):
    calculated_offset = _calculate_source_kitten_compatible_offset(offset, text)
    text = _cut_calculated_offset_difference(offset, calculated_offset, text)
    source_files = _source_files(file, project_directory)

    cmd = [
        "sourcekitten",
        "complete",
        "--text", text,
        "--offset", str(calculated_offset),
        "--"
    ] + _sdk_and_target() + source_files

    return _execute(cmd, _json_parse)

# Cursor info. Calls sourcekitten to get details for what the cursor is
# postioned on. E.g. to get info for the likes of when you hover over something
# in Xcode
#
# For example, offset could point to "Banana" and the returned details would say
# where the "Banana" class is defined
#
# Sourcekitten takes a command like the following:
# ```
# sourcekitten request --yaml 'key.request: source.request.cursorinfo
# key.sourcefile: "/Users/dan2552/projects/SourceKittenSubl/test/data/MonkeyExample/Monkey.swift"
# key.offset: 78
# key.compilerargs:
# - "-sdk"
# - "/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk"
# - "-target"
# - "x86_64-apple-ios10.0"
# - "/Users/dan2552/projects/SourceKittenSubl/test/data/MonkeyExample/Monkey.swift"
# - "/Users/dan2552/projects/SourceKittenSubl/test/data/MonkeyExample/Banana.swift"
# ' 2>/dev/null
# ```
def cursor_info(offset, file, project_directory, text):
    tmp_file = _create_temp_file(text)

    source_files = _source_files(file, project_directory) + [tmp_file]
    compilerargs = _sdk_and_target() + source_files

    yaml_contents = \
        yaml.generate_line("key.request", "source.request.cursorinfo") + \
        yaml.generate_line("key.sourcefile", tmp_file, True) + \
        yaml.generate_line("key.offset", offset) + \
        yaml.generate_line("key.compilerargs", compilerargs, True) \

    cmd = [
        "sourcekitten",
        "request",
        "--yaml",
        yaml_contents
    ]

    output = _execute(cmd, _json_parse)
    _remove_temp_file()
    return output

# This temp file path is used for unsaved current file requests (excluding the
# `.complete` function)
def temp_file_path():
    return "/tmp/SourceKittenSublTemp.swift"

def _sdk_and_target():
    return [
        "-sdk", _sdk(),
        "-target", _target()
    ]

def _sdk():
    return "/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk"

def _target():
    return "x86_64-apple-ios10.0"

def _execute(cmd, result_handler):
    # Converting to a string and back is a little hack to let lru_cache work
    # as it only works on hashable arguments.
    return _execute_cached("§§§".join(cmd), result_handler)

@functools.lru_cache(maxsize=128)
def _execute_cached(cmd, result_handler):
    # print(cmd.replace("§§§", " "))
    cmd = cmd.split("§§§")
    with Popen(cmd, stdout=PIPE, stderr=PIPE) as p:
        # print(p.stdout.peek())
        result = result_handler(p.stdout)
    return result

def _json_parse(stdout):
    try:
        results = list(ijson.items(stdout,''))[0]
        return results
    except ijson.backends.python.UnexpectedSymbol:
        return []

def _source_files(file, project_directory, keep_original_file=None):
    source_files = swift_project.source_files(project_directory)
    if keep_original_file != True:
        source_files = _filter_file_from_list(file, source_files)
    return list(source_files)

# When a file is unsaved, you don't want the persisted file passed into
# SourceKitten
def _filter_file_from_list(file, source_files):
    return filter(lambda x: x != file, source_files)

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

def _create_temp_file(text):
    path = temp_file_path()
    with open(path, "w") as text_file:
        text_file.write(text)
    return path

def _remove_temp_file():
    os.remove(temp_file_path())
