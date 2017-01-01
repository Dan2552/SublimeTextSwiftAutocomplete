import unittest
import path_helper
import file_contents_helper
import source_kitten

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
    def test_changed_code_on_unsaved(self):
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
    def test_midword(self):
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
    def test_midword_type(self):
        offset = 36

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
    def test_spaced_project(self):
        project_directory = path_helper.spaced_example_directory()
        file = ""
        text = "\"\"."
        offset = 3
        output = source_kitten.complete(offset, file, project_directory, text)

        self.assertTrue(len(output) > 0)
