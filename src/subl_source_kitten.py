from . import source_kitten
from . import sourcekit_xml_to_html
import re
import itertools
import cgi
import threading
import operator
import time

# Same as `.complete` but will try two autocompletions:
# 1) as normal
# 2) with all `import`s stripped - faster
#
# If (1) runs within a second, the returned result will use that. If not, the
# result be the value of (2).
def complete_with_haste(offset, file, project_directory, text):
    results = {}

    def repl(m):
        return ' ' * len(m.group())
    stripped_text = re.sub(r'^(\s?import \w+\s?)($|;)', repl, text, flags=re.MULTILINE)

    full = lambda : operator.setitem(results, "full", complete(offset, file, project_directory, text))
    stripped = lambda : operator.setitem(results, "stripped", complete(offset, file, project_directory, stripped_text))
    second = lambda : time.sleep(1)
    t1 = threading.Thread(target=full)
    t2 = threading.Thread(target=stripped)
    t3 = threading.Thread(target=second)
    t1.start()
    t2.start()
    t3.start()

    t2.join()
    if not t1.is_alive():
        return results["full"]
    t3.join()
    if not t1.is_alive():
        return results["full"]
    return results["stripped"]


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

    name_text = _popup_section_from_dict("Name", "key.name", output)
    type_text = _popup_section_from_dict("Type", "key.typename", output)
    group_text = _popup_section_from_dict("Group", "key.groupname", output)

    full_decl = _popup_section_from_dict("Declaration", "key.doc.full_as_xml", output, True, r'.*?(<Declaration[^>]*?>.*?</Declaration>).*?', r'<CommentParts>.*?</CommentParts>')
    short_decl = _popup_section_from_dict("Declaration", "key.annotated_decl", output, True)

    # Generate html for the <Abstract> section of the xml
    abstract = _popup_section_from_dict("Abstract", "key.doc.full_as_xml", output, True, r'.*?(<Abstract[^>]*?>.*?</Abstract>).*?')

    # Generate html for the <Discussion> section of the xml
    discussion = _popup_section_from_dict("Discussion", "key.doc.full_as_xml", output, True, r'.*?(<Discussion[^>]*?>.*?</Discussion>).*?')

    source_loc_text = _source_location_popup_section(file, project_directory, output)

    declaration_text = full_decl
    if len(short_decl) > len(full_decl):
        declaration_text = short_decl

    popup_text = name_text + type_text + source_loc_text + declaration_text + abstract + discussion

    # If we don't have any content, return an empty string
    if popup_text == "":
        return ""

    # Return the content prefixed by the CSS
    return sourcekit_xml_to_html.css + popup_text

def source_location_link(offset, file, project_directory, text):
    dictionary = source_kitten.cursor_info(offset, file, project_directory, text)
    href, relative_path_with_offset = _source_location_paths(file, project_directory, dictionary)
    return href

def _source_location_popup_section(file, project_directory, dictionary):
    href, relative_path_with_offset = _source_location_paths(file, project_directory, dictionary)
    if href == "":
        return ""
    value = "<a href=\"" + href + "\">" + relative_path_with_offset + "</a>"
    return _popup_section("Location", value)

def _source_location_paths(file, project_directory, dictionary):
    filepath = _value_or_empty_string("key.filepath", dictionary)
    offset = _value_or_empty_string("key.offset", dictionary)
    length = _value_or_empty_string("key.length", dictionary)
    if filepath == "":
        return ["", ""]
    offset = offset + 1

    # Current file
    if source_kitten.temp_file_path() in filepath:
        filepath = file

    relative_path = filepath.replace(project_directory + "/", "")
    relative_path_with_offset = relative_path + ":1:" + str(offset)
    absolute_path_with_offset = filepath + ":1:" + str(offset)
    href = absolute_path_with_offset + "-" + str(length)
    return [href, relative_path_with_offset]

# If tag_filter is set, then it is used in a regex match, where the first match
# is used as the section of XML to convert to HTML.
#
# If wipe_filter is set, then it is used as a regex replace with a blank string. This
# Allows for specific tags to be filtered, but to remove contents within those tags
# as needed. This operation is performed after tag_filter.
def _popup_section_from_dict(title, key, dictionary, xml=None, tag_filter=None, wipe_filter=None):
    value = _value_or_empty_string(key, dictionary)

    if value == "":
        return ""

    if xml == True:
        if tag_filter != None:
            m = re.match(tag_filter, value)
            value = ""
            if m != None:
                value = m.group(1)
        if wipe_filter != None:
            value = re.sub(wipe_filter, "", value)
        if value == "":
            return value
        value = sourcekit_xml_to_html.to_html(value)
    else:
        value = "" + cgi.escape(value) + ""

    return _popup_section(title, value)

def _popup_section(title, value):
    value = "<span class='title'>" + title + "</span>" + "<div class='section'>" + value + "</div>"
    return value

def _value_or_empty_string(key, dictionary):
    if not key in dictionary:
        return ""
    return dictionary[key]

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
