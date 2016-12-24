import source_kitten
import re
import itertools

# Returns a 2D array looking something like:
# [
#   ["tree\tInt", "tree"],
#   ["color\tBool", "color"],
# ]
# i.e. to be used by Sublime's on_query_completions
def complete(offset, file, project_directory, text):
    collection = source_kitten.complete(offset, file, project_directory, text)
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
        _sourcetext(item["sourcetext"])
    ]

# SourceKitten will give suggestions like these:
#
# monkey.eat(<#T##banana: Banana##Banana#>)
# monkey.give(banana: <#T##Banana#>, toMonkey: <#T##Monkey#>)
#
# and Sublime expects something more like these:
#
# monkey.eat(${0:<banana: Banana>})
# monkey.give(banana: ${0:<Banana>}, toMonkey: ${1:<Monkey>})
def _sourcetext(text):
    count_iterator = itertools.count()
    next(count_iterator)
    return re.sub(r"<#T##(.+?)#>",
                  lambda x: _sourcetext_substitution(x, count_iterator),
                  text)

def _sourcetext_substitution(regex, count_iterator):
    number = next(count_iterator)
    group = regex.groups()[0].split("#")[0]
    return "${" + str(number) + ":<" + group + ">}"
