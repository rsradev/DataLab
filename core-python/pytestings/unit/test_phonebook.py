import unittest

from phonebook import Phonebook


class PhonebookTest(unittest.TestCase):
    def setUp(self) -> None:
        self.phonebook = Phonebook()

    def test_lookup_by_name(self):
        
        self.phonebook.add('Ivan', '123456')
        self.phonebook.add('Petr', '654321')
        number_ivan = self.phonebook.lookup('Ivan')
 
        self.assertEqual(number_ivan, '123456')
        self.assertEqual(self.phonebook.lookup('Petr'), '654321')

    def test_missing_name(self):
        with self.assertRaises(KeyError):
            self.phonebook.lookup('missing')
    
    @unittest.skip("poor example")
    def test_empty_phonebook_is_consistent(self):
        self.assertTrue(self.phonebook.is_consistent())

    def test_is_consistent_with_different_entries(self):
        self.phonebook.add('Ivan', '123456')
        self.phonebook.add('Petr', '012323')
        self.assertTrue(self.phonebook.is_consistent())     
    
    def test_is_consistent_with_duplicate_entries(self):
        self.phonebook.add('Ivan', '123456')
        self.phonebook.add('Petr', '012323')
        self.phonebook.add('Alex', '123456')
        self.assertFalse(self.phonebook.is_consistent())    

    def test_is_consistent_with_duplicate_prefix(self):
        self.phonebook.add('Ivan', '123456')
        self.phonebook.add('Petr', '012323')
        self.phonebook.add('Alex', '123')
        self.assertFalse(self.phonebook.is_consistent())
