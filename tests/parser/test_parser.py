import os
import unittest

from towerbooks import BookParser
from towerbooks import models
from towerbooks import exceptions

class BookTestClass(object):
    pass

class ChapterTestClass(object):
    pass

class TestParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls, *args, **kwargs):
        cls.parser_class = BookParser
        currentdir = os.path.abspath(os.path.dirname(__file__))
        cls.examples_dir = os.path.join(os.path.abspath(os.path.join(currentdir, os.pardir)), 'examples')

        with open(os.path.join(cls.examples_dir, 'README.txt'), 'r') as _file:
            cls.readme_content = _file.read().replace('\r\n', '')

    def test_contructor_with_valid_orm_args(self, *args, **kwargs):
        parser = self.parser_class(**dict(
                                models=dict(
                                        book='tests.parser.test_parser.BookTestClass',
                                        chapter='tests.parser.test_parser.ChapterTestClass',)
                                )
                            )
        self.assertTrue(parser.book_model is BookTestClass)
        self.assertTrue(parser.chapter_model is ChapterTestClass)

    def test_contructor_with_invalid_orm_book_module(self, *args, **kwargs):
        parser_args = dict(
                        models=dict(
                            book='tests.parser.test_par.BookTestClass',
                            chapter='tests.parser.test_parser.ChapterTestClass',)
                        )
        self.assertRaises(exceptions.InvalidOrmModule, BookParser.__init__, self.parser_class(), **parser_args)

    def test_constructor_with_invalid_orm_chapter_module(self, *args, **kwargs):
        parser_args = dict(
                        models=dict(
                            book='tests.parser.test_parser.BookTestClass',
                            chapter='tests.test_pars.ChapterTestClass',)
                        )
        self.assertRaises(exceptions.InvalidOrmModule, BookParser.__init__, self.parser_class(), **parser_args)

    def test_contructor_with_invalid_orm_book_class(self, *args, **kwargs):
        parser_args = dict(
                        models=dict(
                            book='tests.parser.test_parser.BookClazz',
                            chapter='tests.parser.test_parser.ChapterClazz',)
                        )
        self.assertRaises(exceptions.InvalidOrmClass, BookParser.__init__, self.parser_class(), **parser_args)

    def test_constructor_with_invalid_orm_chapter_class(self, *args, **kwargs):
        parser_args = dict(
                        models=dict(
                            book='tests.parser.test_parser.BookTestClass',
                            chapter='tests.parser.test_parser.ChapterClazz',)
                        )
        self.assertRaises(exceptions.InvalidOrmClass, BookParser.__init__, self.parser_class(), **parser_args)

    def test_constructor_with_no_orm_args(self, *args, **kwargs):
        parser = self.parser_class()
        self.assertTrue(parser.book_model is models.Book)
        self.assertTrue(parser.chapter_model is models.Chapter)

    def test_parser_with_invalid_file_path(self, *args, **kwargs):
        parser = self.parser_class()
        parser.parse('./README.mds')
        self.assertRaises(exceptions.InvalidFile, list, parser.content)

    def test_parser_with_valid_file_paths(self, *args, **kwargs):
        parser = self.parser_class()
        self.path = os.path.join(self.examples_dir, 'README.txt')
        parser.parse(self.path)
        self.assertEqual(self.readme_content, ''.join(list(parser.content)))

    def test_parser_with_valid_file_objects(self, *args, **kwargs):
        parser = self.parser_class()
        with open(os.path.join(self.examples_dir, 'README.txt'), 'rb') as _file:
            parser.parse(_file)
            self.assertEqual(self.readme_content, ''.join(list(parser.content)))
