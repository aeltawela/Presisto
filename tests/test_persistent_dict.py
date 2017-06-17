import unittest

from presisto.presistentdict import PersistentDict


class TestPersistentDict(unittest.TestCase):
    def test_creation(self):
        pd = PersistentDict()
        self.assertIsInstance(pd, PersistentDict)

    def test_multiple_creation(self):
        pd1 = PersistentDict()
        pd2 = PersistentDict()
        self.assertIsInstance(pd1, PersistentDict)
        self.assertIsInstance(pd2, PersistentDict)

        pd3 = PersistentDict('./.data2')
        pd4 = PersistentDict('./.data2')
        self.assertIsInstance(pd3, PersistentDict)
        self.assertIsInstance(pd4, PersistentDict)

        pd5 = PersistentDict('.\.data2')
        pd6 = PersistentDict('.\.data2')
        self.assertIsInstance(pd5, PersistentDict)
        self.assertIsInstance(pd6, PersistentDict)

    def test_read_not_exist(self):
        pd = PersistentDict()

        value = pd.get("not_exist", None)
        self.assertIsNone(value)

        with self.assertRaises(KeyError) as context:
            value = pd['not_exist']

    def test_write_read(self):
        pd = PersistentDict()
        key1 = 'obj1'
        key2 = (5, 4, 3, [2, 3, 4], {'a': 1, 'b': 2})
        value1 = b'string1'
        value2 = dict(a=1, b=2)

        pd[key1] = value1
        self.assertEqual(pd[key1], value1)
        pd[key2] = value2
        self.assertEqual(pd[key2], value2)

    def test_in(self):
        pd = PersistentDict()
        key1 = 'obj1'
        value1 = b'string1'

        pd[key1] = value1
        self.assertIn(key1, pd)

    def test_len(self):
        pd = PersistentDict()
        self.assertIsNotNone(len(pd))

    def test_iter(self):
        pd = PersistentDict()

        for key, value in pd:
            self.assertIsNotNone(key)


if __name__ == '__main__':
    unittest.main()
