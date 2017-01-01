import unittest
import xcode_project_reader
import path_helper
from xcode_project_reader import XcodeProjectReader

class TestXcodeProjectReader(unittest.TestCase):
    def test_targets(self):
        project = XcodeProjectReader(path_helper.xcode_example_project())
        output = list(project.targets())
        expectation = ['Example', 'ExampleTests', 'ExampleUITests']
        self.assertEqual(output, expectation)
