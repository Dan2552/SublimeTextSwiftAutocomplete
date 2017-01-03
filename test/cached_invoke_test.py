import unittest
import cached_invoke
import os.path

class TestCachedInvoke(unittest.TestCase):
    def test_executable_path(self):
        path = cached_invoke.executable_path()
        self.assertTrue(os.path.isfile(path))
