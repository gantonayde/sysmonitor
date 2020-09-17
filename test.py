import unittest
from sysmonitor import get_mem_load, get_proc_by_memory, get_proc_details


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
    
    def test_proc_details(self):
        """
        Test that process details can be obtained.
        """ 
        self.assertTrue(get_proc_details(get_proc_by_memory().index.values[0]))

if __name__ == '__main__':
    unittest.main()


