import inspect


def strip_html(s):
    from xml.etree.ElementTree import fromstring
    from html import unescape
    return unescape("".join(fromstring("<root>%s</root>" % s).itertext()))


class Hex(int):

    def __str__(self):
        return "%X" % self

    def __repr__(self):
        return "0x%x" % self


class Token(str):

    def __new__(cls, name):
        return super().__new__(cls, "<%s>" % name.strip("<>"))

    def __repr__(self):
        return self


def __LOCATION__():
    frame = inspect.getframeinfo(inspect.stack()[1][0])
    return "%s @ %s:%s" % (frame.function, frame.filename, frame.lineno)


def get_all_subclasses(cls):
    _all = cls.__subclasses__() + [rec_subclass
                                   for subclass in cls.__subclasses__()
                                   for rec_subclass in get_all_subclasses(subclass)]
    return [subclass for subclass in _all if not hasattr(subclass, "_%s__is_mixin" % subclass.__name__)]


def stack_level_to_get_out_of_file():
    frame = inspect.currentframe().f_back
    filename = frame.f_code.co_filename
    stack_levels = 1
    while frame.f_code.co_filename == filename:
        stack_levels += 1
        frame = frame.f_back
    return stack_levels
