# SourceKittenSubl

This project is an attempt at adding Swift autocomplete into Sublime Text 3, using [SourceKitten](https://github.com/jpsim/SourceKitten).

It doesn't work too great at the moment, but the source is simple so hopefully it should be easy to contribute to. I'm open for discussion on the repository issues.

## Installation

- Install SwiftKitten (`brew install sourcekitten`)
- Clone this repository to the Sublime packages directory

## Usage

- Open your project top-most directory in Sublime (e.g. `cd ~/projects/MyProject && subl .`)

## How it works

- `main.py`: this file is entry point to the application - `on_query_completions` is an event handler method provided by Sublime Text's API, so Sublime Text will call the method when attempting to autocomplete.
- `subl_source_kitten.py` is purely to convert output from SourceKitten into Sublime autocompletions.
- `source_kitten.py` communicates with the `sourcekitten` - exactly in the same way as you would from a bash shell. Parses the output from JSON into Python objects.

## What works

- Cross-file lookup. All the project `*.swift` files are passed as arguments to the compiler arguments of SourceKitten.

## Needs fixing

- Autocomplete doesn't work on un-saved files (this probably isn't useful until this is fixed)
- Use xcodeproj file for project files when available
- Work out how to make it compatible with imported Frameworks
- Speed up
- Unhardcode SDK and target
- Cleanup debug `print` calls
