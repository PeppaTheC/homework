from siam_meta import SiamMeta, SiamObj
import unittest


class TestSiamMeta(unittest.TestCase):
    def test_singletons(self):
        for a, b, c in zip(range(10), range(10), range(10)):
            unit1 = SiamObj(a, b, c)
            unit2 = SiamObj(a, c, c)
            unit3 = SiamObj(a, b, a=c)
            self.assertIs(unit1, unit2)
            self.assertIs(unit1, unit3)
        for a, b, c in zip(range(10), range(10), range(10)):
            unit1 = SiamObj(a, b, c + 1)
            unit2 = SiamObj(a, b, c)
            self.assertIsNot(unit1, unit2)

    def test_connection(self):
        for a, b, c in zip(range(10), range(10), range(10)):
            unit1 = SiamObj(a + 1, b, c)
            unit2 = SiamObj(a, b, c)
            self.assertIs(unit2.a, unit1.connect(a, b, c).a)

    def test_pool(self):
        instance_list = []
        for i in range(10):
            instance_list.append(SiamObj(i, '2', a=1))
        for instance in instance_list:
            self.assertEqual(len(instance_list), len(instance.pool))
        for _ in range(9):
            del instance_list[0]
            self.assertEqual(len(instance_list), len(instance_list[0].pool))


if __name__ == '__main__':
    unittest.main()
