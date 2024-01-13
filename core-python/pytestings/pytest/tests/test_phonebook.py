from phonebook import Phonebook

def test_lookup_by_name():
    phonebook = Phonebook()
    phonebook.add('Ivan', '123456')
    number = phonebook.lookup('Ivan')
    assert '123456' == number  


def test_phonebook_contains_all_names():
    phonebook = Phonebook()
    phonebook.add('Ivan', '123456')
    assert 'Ivan' in phonebook.names()
    