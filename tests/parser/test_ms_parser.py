from towerbooks import MSParser

from .test_parser import TestParser

class TestMSParser(TestParser):

    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super(TestMSParser, cls).setUpClass(*args, **kwargs)
        cls.parser_class = MSParser

    def test_regex(self, *args, **kwargs):
        pass