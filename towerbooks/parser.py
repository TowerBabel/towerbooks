import importlib

from . import exceptions
from . import models

class BookParser(object):
    """
        A BookParser object will parse a list of files
        and return an ORM style Data Model as 
        directed through the contructor arguments
    """
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
        try:
            return _file.read().replace('\r\n','')
        except AttributeError as ae1:
            try:
                with open(_file, 'r') as __file:
                    return __file.read().replace('\r\n', '')
            except IOError as io1:
                raise exceptions.InvalidFile("The file {} cannot be opened".format(_file))

    def parse(self, _file, *args, **kwargs):
        self.content = self._read_file(_file)

class MSParser(BookParser):

    def __init__(self, *args, **kwargs):
        super(MSParser, self).__init__(*args, **kwargs)

    def parse(self, _file, *args, **kwargs):
        super(MSParser, self).parse(_file)