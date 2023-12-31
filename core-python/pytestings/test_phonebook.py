import unittest

from phonebook import Phonebook


class PhonebookTest(unittest.TestCase):
    def test_lookup_by_name(self):
        phonebook = Phonebook()
        phonebook.add('Ivan', '123456')
        number = phonebook.lookup('Ivan')

        self.assertEqual(number, '123456')

    def test_missing_name(self):
        phonebook = Phonebook()

        with self.assertRaises(KeyError):
            phonebook.lookup('missing')