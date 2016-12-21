import os
from os import popen

# Given a project directory, returns a collection of *.swift files
#
# - parameter project_directory: String path of project
# - returns: List
def source_files(project_directory):
    # TODO: here we could introduce xcodeproj detection
    return _source_files_from_simple_pattern_matching(project_directory)

# Given a project directory, returns a collection of *.swift files by launching
# a `find` process.
#
# - parameter project_directory: String path of project
# - returns: List
def _source_files_from_simple_pattern_matching(project_directory):
    cmd = "find " + project_directory + " -name '*.swift'"
    rows = popen(cmd, "r").readlines()
    return rows
