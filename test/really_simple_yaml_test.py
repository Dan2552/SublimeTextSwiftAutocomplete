import unittest
from src import really_simple_yaml as yaml

class TestReallySimpleYaml(unittest.TestCase):
    def test_generate_line_basic(self):
        output = yaml.generate_line("key", "value")
        expectation = "\nkey: value"
        self.assertEqual(output, expectation)

    def test_generate_line_with_quotes(self):
        output = yaml.generate_line("key", "value", True)
        expectation = "\nkey: \"value\""
        self.assertEqual(output, expectation)

    def test_generate_line_with_number_input(self):
        output = yaml.generate_line("key", 5)
        expectation = "\nkey: 5"
        self.assertEqual(output, expectation)

    def test_generate_line_with_list_as_value(self):
            output = yaml.generate_line("key", ["value1", 2])
            expectation = "\nkey: \n- value1\n- 2"

            self.assertEqual(output, expectation)

    def test_generate_line_with_list_as_value_with_quotes(self):
        output = yaml.generate_line("key", ["value1", 2], True)
        expectation = "\nkey: \n- \"value1\"\n- 2"

        self.assertEqual(output, expectation)
