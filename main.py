from .module_loader import module_loader
module_loader.load(globals())
import sublime, sublime_plugin
from sublime import Region
import requests
import subl_source_kitten

class SublCompletions(sublime_plugin.EventListener):
    # Sublime Text will call this method when trying to autocomplete
    def on_query_completions(self, view, prefix, locations):
        offset = locations[0]
        file = view.file_name()
        if not file.endswith(".swift"):
            return None
        project_directory = view.window().folders()[0]
        text = view.substr(Region(0, view.size()))
        suggestions = subl_source_kitten.complete(offset, file, project_directory, text)
        return (suggestions, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)
