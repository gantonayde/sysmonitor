#!/usr/bin/python3

import unittest
from sysmonitor import get_mem_load, get_proc_by_memory, get_details_with_shell

class TestSysmonitor(unittest.TestCase):

    def test_mem_load(self):
        """
        Test that memory load can be measured.
        """
        self.assertTrue(get_mem_load())

    def test_proc_list(self):
        """
        Test that a list of processes can be obtained.
        """
        self.assertTrue(len(get_proc_by_memory().index.values))

    def test_get_details_with_shell(self):
        """
        Test that process shell commands can be executed.
        Test if returned object is an instance of a string.
        """
        test_cmd = 'echo Hello'
        self.assertTrue(get_details_with_shell(test_cmd))
        self.assertIsInstance(get_details_with_shell(test_cmd), str)

if __name__ == '__main__':
    unittest.main()

