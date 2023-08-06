class I3configgerException(Exception):
    """Main exception with log style string formatting enhancement"""
    def __init__(self, *args, **kwargs):
        try:
            # noinspection PyArgumentList
            super().__init__(args[0] % (args[1:]), **kwargs)
        except:
            # noinspection PyArgumentList
            super().__init__(*args, **kwargs)


class BuildError(I3configgerException):
    pass


class ConfigError(I3configgerException):
    pass


class DuplicateKey(I3configgerException):
    pass


class MalformedAssignment(I3configgerException):
    pass


class MessageError(I3configgerException):
    pass


class PartialsError(I3configgerException):
    pass


class ParseError(I3configgerException):
    pass
