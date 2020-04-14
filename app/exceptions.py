class BadLineError(Exception):
    pass


class LessThanMinimalDurationError(BadLineError):
    pass


class InvalidTimeError(BadLineError):
    pass


class EmptyLineError(Exception):
    pass


class InvalidTimelogError(Exception):
    pass
