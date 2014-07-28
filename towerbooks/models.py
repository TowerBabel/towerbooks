class Image(object):
    pass

class Chapter(object):
    pass

class Book(object):

    attrs = set((
        'id',
        'title',
        'authors',
        ))

    def __init__(self, *args, **kwargs):
        for attr in kwargs.viewkeys() & self.attrs:
            setattr(self, attr, kwargs[attr])