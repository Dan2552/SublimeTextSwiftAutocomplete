import re

class XcodeProjectReader():
    def __init__(self, file_path):
        if file_path.endswith(".xcodeproj"):
            file_path = file_path + "/project.pbxproj"
        self.contents = _read(file_path)
        self.target_scopes = self._find_target_scopes()

    # A list of named targets
    #
    # - Returns: e.g. ['Example', 'ExampleTests', 'ExampleUITests']
    def targets(self):
        return map(lambda n: _scope_value("name", n), self.target_scopes)

    # Finds blocks in a pbxproj
    #
    # - parameter scope_type: e.g. PBXBuildFile, PBXNativeTarget
    # - returns: collection of found scopes, [String]
    def _scopes(self, scope_type):
        scope_type_identifier = "isa = " + scope_type + ";"
        type_identifier_indexes = list(_find_all(self.contents, scope_type_identifier))
        return map(lambda x: self._find_wrapping_scope(x), type_identifier_indexes)

    def _find_wrapping_scope(self, index):
        left = self.contents.rfind("= {", 0, index) + 3
        right = self.contents.find("};", index, len(self.contents))
        return self.contents[left:right]

    def _find_target_scopes(self):
        return self._scopes("PBXNativeTarget")


def _read(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

def _find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def _scope_value(key, scope):
    regex = r"name = (.*);"
    matches = re.findall(regex, scope)
    if len(matches) > 0:
        return matches[0]
    return None
