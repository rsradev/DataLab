import pytest
from phonebook import Phonebook


@pytest.fixture
def phonebook():
    phonebook = Phonebook()
    yield phonebook
    phonebook.clear()


def test_lookup_by_name(phonebook):
    phonebook.add('Ivan', '123456')
    number = phonebook.lookup('Ivan')
    assert '123456' == number


def test_phonebook_contains_all_names(phonebook):
    phonebook.add('Ivan', '123456')
    assert phonebook.all_names() == {'Ivan'}


def test_missing_name(phonebook):
    #phonebook.add('Ivan', '123456')
    with pytest.raises(KeyError):
        phonebook.lookup('Ivan')


@pytest.mark.parametrize(
    "entry1,entry2,is_consistent", [
        (('Bob', '12345'), ('Anna', '01123'), True),
        (('Bob', '12345'), ('Sue', '12345'), False),
        (('Bob', '12345'), ('Sanna', '123'), False),
    ]
)


def test_is_consistent(phonebook, entry1, entry2, is_consistent):
    phonebook.add(*entry1)
    phonebook.add(*entry2)
    assert phonebook.is_consistent() == is_consistent