# SourceKittenSubl

This project is an attempt at adding Swift autocomplete into Sublime Text 3, using [SourceKitten](https://github.com/jpsim/SourceKitten).

While it doesn't read Xcode project files, it currently works pretty well for me on my projects. The source of SourceKittenSubl is simple so hopefully it should be easy to contribute to. I'm open for discussion on the repository issues.

![Autocomplete](images/autocomplete.png#1)

![Popup](images/popup.png#1)

## Installation

- Install SourceKitten (`brew install sourcekitten`)
- Clone this repository to the Sublime packages directory
- [Optionally for speed] Install a faster JSON parsing back-end: (`brew install yajl`)

## Usage

- Open your project top-most directory in Sublime (e.g. `cd ~/projects/MyProject && subl .`)

## For developers
- Run the test runner: `./run_tests`

These are the main componenets of the plugin:
- `subl.py`: this file is entry point to the plugin from Sublime - `on_query_completions` is an event handler method provided by Sublime Text's API, so Sublime Text will call the method when attempting to autocomplete.
- `subl_source_kitten.py` is purely to convert output from SourceKitten into a format that can be output in Sublime Text.
- `source_kitten.py` communicates with the `sourcekitten` - exactly in the same way as you would from a bash shell. Parses the output from JSON into Python objects.
- `swift_project.py` deals with the "project" (i.e. which source files should be passed in to SourceKitten)



