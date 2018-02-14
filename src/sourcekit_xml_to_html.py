# This is derived from
# https://github.com/johncsnyder/SwiftKitten/blob/13c32401f16f0e6abd6deb180a9f96c590c27c6a/SwiftKitten.py#L650
# so special thanks to John Snyder for starting this

import re
import xml.etree
from xml.etree import ElementTree

xml_to_html_tags = {
    "Name"              : "strong",   "Abstract"          : "div",
    "Protocol"          : "div",      "InstanceMethod"    : "div",
    "SeeAlsos"          : "div",      "Discussion"        : "span",
    "Declaration"       : "div",      "Class"             : "div",
    "Note"              : "div",      "Para"              : "p",
    "SeeAlso"           : "p",        "Availability"      : "p",
    "zModuleImport"     : "p",        "zAttributes"       : "p",
    "Attribute"         : "p",        "uAPI"              : "a",
    "codeVoice"         : "span",      "newTerm"           : "em",
    "List-Bullet"       : "ul",       "Item"              : "li",
    "AvailabilityItem"  : "em",       "InstanceProperty"  : "div",
    "CodeListing"       : "div",      "reservedWord"      : "b",
    "keyWord"           : "span",     "Property-ObjC"     : "div",
    "kConstantName"     : "em",       "Structure"         : "div",
    "Function"          : "div",      "ClassMethod"       : "div",
    "ClassProperty"     : "div",      "Enumeration"       : "div",
    "Constant"          : "div",      "Parameter"         : "li",
    "Parameters"        : "ul",       "CodeListing"       : "div",
    "zCodeLineNumbered" : "span",     "emphasis"          : "em",
    "Complexity"        : "div",      "USR"               : "span"
}

css = """
<style>
.title {
    color: color(var(--background) blend(var(--foreground) 50%));
}

.section {
    padding-left: 8rem;
    padding-top: -1.3rem;
    padding-bottom: 10px;
}

ul {
    padding-top: 0;
    margin-top: 0;
    margin-bottom: 0.5rem;
}

.zcodelinenumbered {
    display: block;
}

.codelisting {
    padding: 0.5rem;
    background-color: color(var(--background) blend(var(--foreground) 85%));
}

.codevoice {
    background-color: color(var(--background) blend(var(--foreground) 85%));
}

.discussion, li p {
    padding: 0;
    margin: 0;
    display: inline;
}
</style>
"""

def to_html(xml):
    xml = _sanitize(_tweaks(xml))

    root = ElementTree.fromstring(xml)
    removals = []

    for el in root.iter():
        original_tag = el.tag
        if el.tag == "USR":
            removals.append(el)
        el.tag = xml_to_html_tags.get(original_tag, original_tag)
        el.set("class", original_tag.casefold())

        if el.tag == "a":
            if "url" in el.attrib:
                el.attrib["href"] = el.attrib["url"]
                del el.attrib["url"]

    for el in removals:
        root.remove(el)

    converted_xml = str(ElementTree.tostring(root, encoding="utf-8"), "utf-8")

    return css + converted_xml

# Sublime Text minihtml is a bit delicate. So here we remove tags that prevent
# it working as expected.
def _sanitize(text):
    # Sanitize the contents of CDATA elements. We do this before removing the
    # CDATA tags.
    #
    # Example:
    #
    #     <![CDATA[        bytes: count * MemoryLayout<Point>.stride,]]>
    #
    # ...becomes...
    #
    #     <![CDATA[        bytes: count * MemoryLayout&lt;Point>.stride,]]>
    #
    # In English, this RE replaces all '<' characters with the string "&lt;"
    # when they appear between the strings "![CDATA[" and "]]>".
    text = re.sub(r'<(?=(?:(?!(?:!\[CDATA\[|]]>)).)*?\]\]>)', '&lt;', text)

    text = text.replace("<![CDATA[", "")
    text = text.replace("]]>", "")
    text = text.replace("<rawHTML>", "")
    text = text.replace("</rawHTML>", "")
    text = text.replace("<Discussion>", "")
    text = text.replace("</Discussion>", "")
    text = text.replace("<zCodeLineNumbered></zCodeLineNumbered>", "")
    text = text.replace("..<", "..&lt;")
    return text

# The output we get isn't always the best looking, so this function does some
# minor tweaks to make it look a little nicer.
def _tweaks(text):
    text = text.replace("<Direction isExplicit=\"0\">in</Direction>", ": ")
    text = text.replace("<Parameters>", "Parameters:<Parameters>")
    return text
