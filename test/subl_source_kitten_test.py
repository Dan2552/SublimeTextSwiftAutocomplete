import unittest
import path_helper
import subl_source_kitten
import file_contents_helper
import time

class TestSublSourceKitten(unittest.TestCase):
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
        output = subl_source_kitten.complete(offset, file, project_directory, text)

        expectation = [
            ["color\tString", "color"],
            ["flavor\tInt", "flavor"],
        ]

        self.assertEqual(list(output), expectation)

    def test_complete_with_haste_simple(self):
        offset = 121
        project_directory = path_helper.monkey_example_directory()
        file = project_directory + "/Monkey.swift"
        text = file_contents_helper.read(file)
        output = subl_source_kitten.complete_with_haste(offset, file, project_directory, text)

        expectation = [
            ["color\tString", "color"],
            ["flavor\tInt", "flavor"],
        ]

        self.assertEqual(list(output), expectation)

    def test_complete_with_haste_uikit(self):
        text = "import UIKit; class Testing() { func aFunction() {  } } # haste"
        offset = 51
        file = ""
        project_directory = "/dev/null"
        start_time = int(round(time.time() * 1000))
        output = subl_source_kitten.complete_with_haste(offset, file, project_directory, text)
        end_time = int(round(time.time() * 1000))
        print("subl_source_kitten.complete_with_haste - Performance test: ", end_time - start_time, 'ms')
        self.assertTrue(len(list(output)) > 0)

    # When autocompleting a method, you  want the cursor to be able to jump
    # between arguments. Sublime has a feature when dollar-numeric fields such
    # as a snippet does, e.g. $0, $1
    def test_snippet_markers(self):
        file = ""
        text = "Monkey()."
        offset = 9
        project_directory = path_helper.monkey_example_directory()
        output = subl_source_kitten.complete(offset, file, project_directory, text)

        expectation = [
            ['consumedBananas\t[Banana]', 'consumedBananas'],
            ['eat(:)\tVoid', 'eat(${1:<banana: Banana>})'],
            ['give(banana:toMonkey:)\tVoid', 'give(banana: ${1:<Banana>}, toMonkey: ${2:<Monkey>})']
        ]

        self.assertEqual(list(output), expectation)
