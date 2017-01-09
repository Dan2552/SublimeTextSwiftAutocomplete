import source_kitten
import re
import itertools
import sourcekit_xml_to_html
import cgi

# Swift autocomplete
#
# - returns: a 2D array looking something like:
# [
#   ["tree\tInt", "tree"],
#   ["color\tBool", "color"],
# ]
# i.e. to be used by Sublime's on_query_completions
def complete(offset, file, project_directory, text):
    collection = source_kitten.complete(offset, file, project_directory, text)
    return map(_subl_completion, collection)

# Returns markdown, converted from source_kitten.cursor_info. In order to render
# the markdown, it should be passed to the mdpopups dependency
def popup(offset, file, project_directory, text):
    output = source_kitten.cursor_info(offset, file, project_directory, text)

    name_text = _popupSection("Name", "key.name", output)
    type_text = _popupSection("Type", "key.typename", output)
    group_text = _popupSection("Group", "key.groupname", output)

    full_decl = _popupSection("Declaration", "key.doc.full_as_xml", output, True)
    short_decl = _popupSection("Declaration", "key.annotated_decl", output, True)

    declaration_text = full_decl
    if len(short_decl) > len(full_decl):
        declaration_text = short_decl

    popup_text = name_text + type_text + declaration_text

    return popup_text

def _popupSection(title, key, dictionary, xml=None):
    if not key in dictionary:
        return ""
    value = dictionary[key]

    if xml == True:
        value = sourcekit_xml_to_html.to_html(value)
    else:
        value = "" + cgi.escape(value) + ""

    value = "<span class='title'>" + title + "</span>" + "<div class='section'>" + value + "</div>"
    return value

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
