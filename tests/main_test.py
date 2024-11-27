import unittest
import main as m2d

class TestMain(unittest.TestCase):

    def setUp(self):
        # Setup code to run before each test
        pass

    def tearDown(self):
        # Cleanup code to run after each test
        pass

    def test_dra(self):
        self.assertEqual(m2d.determine_rotation_angles((0, 0), (0, 90)), 90)

if __name__ == '__main__':
    unittest.main()