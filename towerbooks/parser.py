from __future__ import with_statement
import importlib
import re

from . import exceptions
from . import models

class Node(list):
    def __init__(self, parent=None):
        self.parent = parent

class NestedParser(object):
    """
        As found on the StackOverflow.com question @
        http://stackoverflow.com/questions/1099178/matching-nested-structures-with-regular-expressions-in-python

        Nested structures can not be matched with Python regex alone, but it is remarkably easy to build a
        basic parser (which can handle nested structures) using re.Scanner

        By default NestedParser matches nested parentheses. You can pass other regex to match other nested
        patterns, such as brackets, []


    """
    def __init__(self, left='\(', right='\)', *args, **kwargs):
        # self.scanner = re.Scanner([
        #     (left, self.left),
        #     (right, self.right),
        #     (r"\s+", None),
        #     (".+?(?=(%s|%s|$))" % (right, left), self.other),
        # ])
        # self.result = Node()
        # self.current = self.result
        pass

    def _parse(self, content):
        self.scanner.scan(content)
        return self.result

    def left(self, scanner, token):
        new = Node(self.current)
        self.current.append(new)
        self.current = new

    def right(self, scanner, token):
        self.current = self.current.parent

    def other(self, scanner, token):
        self.current.append(token.strip())

class BookParser(NestedParser):
    """
        A BookParser object will parse a list of files
        and return an ORM style Data Model as 
        directed through the contructor arguments
    """
    #FILE object buffer size for larger files
    BUFFER_SIZE = 1024

    def __init__(self, *args, **kwargs):
        if kwargs.get('models', None):
            _d = kwargs['models']
            self._validate_user_orm(_d)
        else:
            self.book_model = models.Book
            self.chapter_model = models.Chapter

    def _import_class(self, cls_path, attr):
        try:
            
            mod, cls = cls_path.rsplit('.', 1)
            mod = importlib.import_module(mod)
            setattr(self, attr, getattr(mod, cls))

        except ImportError as ie1:
            raise exceptions.InvalidOrmModule("Error importing module {}".format(mod))
        except AttributeError as ve1:
            raise exceptions.InvalidOrmClass("Error importing class {}".format(cls))

    def _validate_class(self, cls_path, attr):
        self._import_class(cls_path, attr)

    def _validate_user_orm(self, _dict):
        if not all(x in _dict.keys() for x in ['book', 'chapter']):
            raise exceptions.InvalidORM("Missing book or chapter model")

        self._validate_class(_dict['book'], "book_model")
        self._validate_class(_dict['chapter'], "chapter_model")

    def _read_file(self, _file):
        while True:
            try:
                data = _file.read(self.BUFFER_SIZE)
            except AttributeError as ae1:
                try:
                    with open(_file, 'rb') as f:
                        data = f.read(self.BUFFER_SIZE)
                except IOError as io1:
                    raise exceptions.InvalidFile("The file {} cannot be opened".format(_file))
            if data:
                yield data
            break

    def parse(self, _file, *args, **kwargs):
        self.content = self._read_file(_file)

class MSParser(BookParser):

    def __init__(self, *args, **kwargs):
        super(MSParser, self).__init__(*args, **kwargs)

    def parse(self, _file, *args, **kwargs):
        super(MSParser, self).parse(_file)