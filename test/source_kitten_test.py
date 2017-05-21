import unittest
import path_helper
import file_contents_helper
import source_kitten
import time

class TestSourceKitten(unittest.TestCase):
    # Here we test (within the "Monkey" example) that
    #
    # print("Eating the \(banana.
    #                           ^
    # comes up with 2 suggestions:
    # - color (String)
    # - flavor (Int)
    #
    # Formatted as a sublime autocomplete
    def test_complete_simple(self):
        offset = 121
        project_directory = path_helper.monkey_example_directory()
        file = project_directory + "/Monkey.swift"
        text = file_contents_helper.read(file)
        output = source_kitten.complete(offset, file, project_directory, text)

        expectation = [
            ["color\tString", "color"],
            ["flavor\tInt", "flavor"],
        ]

        self.assertEqual(len(output), 2)
        self.assertEqual(output[0]["name"], "color")
        self.assertEqual(output[0]["typeName"], "String")
        self.assertEqual(output[1]["name"], "flavor")
        self.assertEqual(output[1]["typeName"], "Int")

    # When a variable is changed from what is persisted on the file system
    #
    # (i.e. test to ensure unsaved autocomplete is working ok)
    def test_complete_changed_code_on_unsaved(self):
        offset = 162
        project_directory = path_helper.monkey_example_directory()
        file = project_directory + "/Monkey.swift"
        text = file_contents_helper.read(file)
        output = source_kitten.complete(offset, file, project_directory, text)
        self.assertTrue(len(output) > 0)

        text = text.replace("consumedBananas", "consumedBananaz", 1)
        output = source_kitten.complete(offset, file, project_directory, text)
        self.assertTrue(len(output) == 0)

        text = text.replace("consumedBananas", "consumedBananaz", 1)
        output = source_kitten.complete(offset, file, project_directory, text)
        self.assertTrue(len(output) > 0)

    # Midword completions. e.g:
    #
    # print("Eating the \(banana.co
    #                             ^
    def test_complete_midword(self):
        offset = 123

        project_directory = path_helper.monkey_example_directory()
        file = project_directory + "/Monkey.swift"
        text = file_contents_helper.read(file)
        output = source_kitten.complete(offset, file, project_directory, text)

        self.assertTrue(len(output) > 0)
        self.assertEqual(output[0]["name"], "color")
        self.assertEqual(output[0]["typeName"], "String")

    # There's not always a `.` preceeding a possible autocomplete
    #
    # struct Banana {
    #     let color: Strin
    #                    ^
    def test_complete_midword_type(self):
        offset = 80

        project_directory = path_helper.monkey_example_directory()
        file = project_directory + "/Banana.swift"
        text = file_contents_helper.read(file)
        output = source_kitten.complete(offset, file, project_directory, text)

        self.assertTrue(len(output) > 0)

        found_string_as_autocomplete = False
        for entry in output:
            if entry["name"] == "String" and entry["typeName"] == "String":
                found_string_as_autocomplete = True

        self.assertTrue(found_string_as_autocomplete)

    # Test project with spaces in subdirectory name
    def test_complete_spaced_project(self):
        project_directory = path_helper.spaced_example_directory()
        file = ""
        text = "\"\"."
        offset = 3
        output = source_kitten.complete(offset, file, project_directory, text)

        self.assertTrue(len(output) > 0)

    # Tests with UIKit import to check that it works
    #
    # Because it can be slow, also includes printout of how long it takes to autocomplete
    # twice (so as to also test caching)
    def test_complete_performance(self):
        text = "import UIKit; class Testing() { func aFunction() {  } }"
        offset = 51
        file = ""
        project_directory = "/dev/null"

        start_time = int(round(time.time() * 1000))
        output = source_kitten.complete(offset, file, project_directory, text)
        end_time = int(round(time.time() * 1000))

        print("source_kitten.complete - Performance test (1st): ", end_time - start_time, 'ms')

        start_time = int(round(time.time() * 1000))
        source_kitten.complete(offset, file, project_directory, text)
        end_time = int(round(time.time() * 1000))

        print("source_kitten.complete - Performance test (2nd): ", end_time - start_time, 'ms')

        self.assertTrue(len(output) > 0)
        ui_view_controller_entries = filter(lambda n: n["name"] == "UIViewController", output)
        self.assertTrue(len(list(ui_view_controller_entries)) > 0)

    # Cursor popover
    # eat(_ banana: Banana) {
    #                 ^
    def test_cursor_info(self):
        offset = 78
        project_directory = path_helper.monkey_example_directory()
        file = project_directory + "/Monkey.swift"
        text = file_contents_helper.read(file)

        output = source_kitten.cursor_info(offset, file, project_directory, text)

        self.assertEqual(output["key.name"], "Banana")
        self.assertEqual(output["key.typename"], "Banana.Type")
        self.assertEqual(output["key.filepath"], project_directory + "/Banana.swift")
        self.assertEqual(output["key.offset"], 7)
        self.assertEqual(output["key.length"], 6)

    def test_cursor_info_unsaved(self):
        offset = 31
        project_directory = path_helper.monkey_example_directory()
        file = project_directory + "/Monkey.swift"
        text = file_contents_helper.read(file)
        text = text.replace("consumedBananas", "consumedBananaz", 1)

        output = source_kitten.cursor_info(offset, file, project_directory, text)

        self.assertEqual(output["key.name"], "consumedBananaz")

    # Issue raised by GitHub user @ccampbell
    # https://github.com/Dan2552/SourceKittenSubl/issues/19
    def test_copyright_symbol(self):
        file = ""
        text = "// ©©\nvar test = 10\ntest."
        offset = len(text)
        project_directory = "/dev/null"
        output = source_kitten.complete(offset, file, project_directory, text)

        self.assertTrue(len(list(output)) > 0)
        self.assertEqual(output[0]['sourcetext'], "advanced(by: <#T##Int#>)")
