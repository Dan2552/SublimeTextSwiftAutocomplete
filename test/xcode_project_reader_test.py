from src.xcode_project_reader import XcodeProjectReader
from helpers import path_helper
import unittest

class TestXcodeProjectReader(unittest.TestCase):
    def test_targets(self):
        project = XcodeProjectReader(path_helper.xcode_example_project())
        output = list(project.targets())
        expectation = ['Example', 'ExampleTests', 'ExampleUITests']
        self.assertEqual(output, expectation)
