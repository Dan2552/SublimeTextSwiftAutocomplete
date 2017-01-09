from .dependencies import dependencies
dependencies.load()

import sublime, sublime_plugin
from sublime import Region
import subl_source_kitten

# Sublime Text will will call `on_query_completions` itself
class SublCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        file = view.file_name()
        if not _is_swift(file):
            return None

        offset = locations[0]
        project_directory = _project_directory(view)
        text = _view_text(view)
        suggestions = subl_source_kitten.complete(offset, file, project_directory, text)
        return (suggestions, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

    def on_hover(self, view, point, hover_zone):
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
            self.view.window().open_file(url, sublime.ENCODED_POSITION | sublime.TRANSIENT)

    def on_hide(self):
        pass

def _project_directory(view):
    if len(view.window().folders()) > 0:
        return view.window().folders()[0]
    return ""

def _view_text(view):
    return view.substr(Region(0, view.size()))

def _is_swift(file):
    return file == None or file.endswith(".swift")
