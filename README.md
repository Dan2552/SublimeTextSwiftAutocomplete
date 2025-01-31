> [!WARNING]
> This probably hasn't worked for years :) don't bother trying

# SublimeTextSwiftAutocomplete

Swift autocomplete and documentation in Sublime Text 3, using [SourceKitten](https://github.com/jpsim/SourceKitten).

![Autocomplete](images/autocomplete.png#1)

![Popup](images/popup.png#1)

## Installation

- Install SourceKitten (`brew install sourcekitten`)
- Clone this repository to the Sublime packages directory

## Usage

- Open your project top-most directory in Sublime (e.g. `cd ~/projects/MyProject && subl .`)

## Notes

- SublimeTextSwiftAutocomplete doesn't read Xcode project files, but instead uses the top-most directory open in Sublime.
- The source of SublimeTextSwiftAutocomplete is simple so hopefully it should be easy to contribute to (please do!). I'm open for discussion on the repository issues if you want to discuss / you're at all unsure how to approach a problem.

## For contributing
- Run the test runner: `./run_tests`
- If you're contributing, try to write a test to capture the problem

These are the main components of the plugin:
- `subl.py`: this file is entry point to the plugin from Sublime - `on_query_completions` is an event handler method provided by Sublime Text's API, so Sublime Text will call the method when attempting to autocomplete.
- `subl_source_kitten.py` is purely to convert output from SourceKitten into a format that can be output in Sublime Text.
- `source_kitten.py` communicates with the `sourcekitten` - exactly in the same way as you would from a bash shell. Parses the output from JSON into Python objects.
- `swift_project.py` deals with the "project" (i.e. which source files should be passed in to SourceKitten)
