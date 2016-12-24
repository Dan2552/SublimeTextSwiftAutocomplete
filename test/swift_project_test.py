import unittest
import path_helper
import swift_project

class TestSourceKitten(unittest.TestCase):
    # Test with a simple project directory
    # (i.e. without xcodeproj)
    def test_source_files_simple_project(self):
        project_directory = path_helper.monkey_example_directory()

        output = swift_project.source_files(project_directory)

        expectation = [
            project_directory + "/Banana.swift",
            project_directory + "/Monkey.swift"
        ]

        self.assertEqual(list(output), expectation)
