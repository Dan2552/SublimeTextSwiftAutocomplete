import source_kitten

# Returns a 2D array looking something like:
# [
#   ["tree\tInt", "tree"],
#   ["color\tBool", "color"],
# ]
# i.e. to be used by Sublime's on_query_completions
def complete(offset, file, project_directory):
    collection = source_kitten.complete(offset, file, project_directory)
    return map(_subl_completion, collection)

# An item will look something like this:
#
# {
#   "descriptionKey" : "tree",
#   "kind" : "source.lang.swift.decl.var.instance",
#   "name" : "tree",
#   "sourcetext" : "tree",
#   "typeName" : "Int",
#   "associatedUSRs" : "s:vC1b6Banana4treeSi",
#   "moduleName" : "b",
#   "context" : "source.codecompletion.context.thisclass"
# }
#
# and this function will change it to something like this:
#
# ["tree\tInt", "tree"]
def _subl_completion(item):
    return [
        item["name"] + "\t" + item["typeName"],
        item["sourcetext"]
    ]
