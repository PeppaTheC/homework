import unittest
from timer_property import timer_property, Message
import time


class TestTimerProperty(unittest.TestCase):
    def test_creation(self):
        m1 = Message()
        m2 = Message()
        self.assertNotEqual(m1.read, m2.read)

    def test_setter(self):
        m1 = Message()
        for i in range(10):
            m1.msg = i
            self.assertEqual(m1.read, i)
        m1.msg = 42
        time.sleep(2)
        self.assertNotEqual(m1.read, 42)

    def test_getter_cache(self):
        m1 = Message()
        for i in range(5):
            initial_m1 = m1.read
            self.assertEqual(initial_m1, m1.read)
            time.sleep(2)
            self.assertNotEqual(initial_m1, m1.read)


if __name__ == '__main__':
    unittest.main()
