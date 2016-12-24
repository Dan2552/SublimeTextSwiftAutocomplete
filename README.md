# SourceKittenSubl

This project is an attempt at adding Swift autocomplete into Sublime Text 3, using [SourceKitten](https://github.com/jpsim/SourceKitten).

It currently works okayish on smaller projects (e.g. [branch](https://github.com/Dan2552/branch)), but the source of SourceKittenSubl is simple so hopefully it should be easy to contribute to. I'm open for discussion on the repository issues.

## Installation

- Install SwiftKitten (`brew install sourcekitten`)
- Clone this repository to the Sublime packages directory

## Usage

- Open your project top-most directory in Sublime (e.g. `cd ~/projects/MyProject && subl .`)

## How it works

- `subl.py`: this file is entry point to the plugin from Sublime - `on_query_completions` is an event handler method provided by Sublime Text's API, so Sublime Text will call the method when attempting to autocomplete.
- `subl_source_kitten.py` is purely to convert output from SourceKitten into Sublime autocompletions.
- `source_kitten.py` communicates with the `sourcekitten` - exactly in the same way as you would from a bash shell. Parses the output from JSON into Python objects.
- `swift_project.py` deals with the "project" (i.e. which source files should be passed in to SourceKitten)

## Running tests
- Run the test runner: `./run_tests`

## What works

- Cross-file lookup. All the project `*.swift` files are passed as arguments to the compiler arguments of SourceKitten.
- Autocomplete on un-saved files

## Needs fixing

- Use xcodeproj file for project files when available
- Work out how to make it compatible with imported Frameworks
- Speed up
- Unhardcode SDK and target
