from .dependencies import dependencies
dependencies.load()

import sublime, sublime_plugin
from sublime import Region
import subl_source_kitten
from threading import Timer

# Sublime Text will will call `on_query_completions` itself
class SublCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        self.view = view
        file = view.file_name()
        if not _is_swift(file):
            return None

        offset = locations[0]
        project_directory = _project_directory(view)
        text = _view_text(view)
        suggestions = subl_source_kitten.complete(offset, file, project_directory, text)
        return (suggestions, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

    def on_hover(self, view, point, hover_zone):
        self.view = view
        file = view.file_name()
        if not _is_swift(file):
            return

        if hover_zone != sublime.HOVER_TEXT:
            return

        project_directory = _project_directory(view)
        text = _view_text(view)

        text = subl_source_kitten.popup(point, file, project_directory, text)

        view.show_popup(text,
                        sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                        point,
                        600,
                        600,
                        self.on_navigate,
                        self.on_hide)

    def on_navigate(self, url):
        if self.view.is_popup_visible():
            self.view.hide_popup()
        filepath, line, offsets = url.split(":")
        column, length = offsets.split("-")
        new_view = self.view.window().open_file(url, sublime.ENCODED_POSITION)

        start_offset = int(column) - 1
        end_offset = start_offset + int(length)
        region = Region(start_offset, end_offset)

        # Add a highlight
        new_view.add_regions("highlight", [region], "comment")

        # Remove highlight after a second
        Timer(1.0, lambda: new_view.add_regions("highlight", [], "comment")).start()

    def on_hide(self):
        pass

class SourceKittenSublDocCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        point = self.view.sel()[0].begin()
        SublCompletions().on_hover(self.view, point, sublime.HOVER_TEXT)

def _project_directory(view):
    if len(view.window().folders()) > 0:
        return view.window().folders()[0]
    return ""

def _view_text(view):
    return view.substr(Region(0, view.size()))

def _is_swift(file):
    return file == None or file.endswith(".swift")
