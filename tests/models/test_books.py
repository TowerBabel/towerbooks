import unittest

from towerbooks.models import Book

class TestBook(unittest.TestCase):

    def test_book_constructor(self, *args, **kwargs):
        _title = 'The Old Man and The Sea'
        _hemingway = 'Ernest Hemingway'
        book = Book(title=_title, authors=[_hemingway], foo='bar')
        self.assertEqual(book.title, _title)
        self.assertTrue(_hemingway in book.authors)
        self.assertRaises(AttributeError, getattr, book, "foo")
