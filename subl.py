from .dependencies import dependencies
dependencies.load()

import sublime, sublime_plugin
from sublime import Region
import subl_source_kitten

# Sublime Text will will call `on_query_completions` itself
class SublCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        offset = locations[0]
        file = view.file_name()

        if file != None and not file.endswith(".swift"):
            return None

        project_directory = view.window().folders()[0]
        text = view.substr(Region(0, view.size()))
        suggestions = subl_source_kitten.complete(offset, file, project_directory, text)
        return (suggestions, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)
