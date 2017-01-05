import subprocess
from subprocess import Popen, PIPE, STDOUT
import ijson
import swift_project
import functools

def complete(offset, file, project_directory, text):
    calculated_offset = _calculate_source_kitten_compatible_offset(offset, text)
    text = _cut_calculated_offset_difference(offset, calculated_offset, text)

    cmd = [
        "sourcekitten",
        "complete",
        "--text", text,
        "--offset", str(calculated_offset),
        "--",
        "-sdk", "/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk",
        "-target", "x86_64-apple-ios10.0"
    ] + list(_source_files(file, project_directory))

    # Converting to a string and back is a little hack to let lru_cache work
    output = _execute("§".join(cmd), _json_parse)
    return output

@functools.lru_cache(maxsize=None)
def _execute(cmd, result_handler):
    cmd = cmd.split("§")
    with Popen(cmd, stdout=PIPE, stderr=STDOUT) as p:
        result = result_handler(p.stdout)
    return result

def _json_parse(stdout):
    try:
        results = list(ijson.items(stdout,''))[0]
        return results
    except ijson.backends.python.UnexpectedSymbol:
        return []

def _source_files(file, project_directory):
    source_files = swift_project.source_files(project_directory)
    source_files = _filter_file_from_list(file, source_files)
    return source_files

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
