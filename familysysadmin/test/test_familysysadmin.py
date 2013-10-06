

import unittest
import time
import familysysadmin.familysysadmin

class TestSQLite(unittest.TestCase):
    def setUp(self):
        pass

    def test_simple(self):
        app = familysysadmin.familysysadmin.FamilySysAdminApp()
        app.MainLoop()

if __name__ == "__main__":
    unittest.main()